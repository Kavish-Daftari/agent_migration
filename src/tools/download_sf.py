from dotenv import load_dotenv 
import os
from pathlib import Path 
import shutil
from typing import List,Optional 
from langchain_core.tools import tool
import snowflake.connector
load_dotenv()
WORKSPACE_DIR = Path("./agent_workspace")
WORKSPACE_DIR.mkdir(exist_ok=True)
@tool
def download_file_from_snowflake(filename: str) -> str:
    """Download a file from Snowflake stage to the workspace."""
    try:
        conn = snowflake.connector.connect(
            user=os.environ["SF_USER"],
            password=os.environ["SF_PASSWORD"],
            account=os.environ["SF_ACCOUNT"],
            warehouse=os.environ["SF_WAREHOUSE"],
            database=os.environ["SF_DATABASE"],
            schema=os.environ["SF_SCHEMA"],
        )
        
        stage = os.environ["SF_STAGE"]
        cur = conn.cursor()
        
        # Download to workspace
        cur.execute(f"GET @{stage}/{filename} file://{WORKSPACE_DIR.as_posix()}")
        result = cur.fetchall()
        
        cur.close()
        conn.close()
        
        # Find the downloaded file (Snowflake may create nested folders)
        matches = list(WORKSPACE_DIR.rglob(filename))
        if matches:
            # Move to workspace root if in nested folder
            source_file = matches[0]
            target_file = WORKSPACE_DIR / filename
            if source_file != target_file:
                shutil.move(str(source_file), str(target_file))
            
            return f"✅ Downloaded {filename} to workspace ({target_file.stat().st_size} bytes)"
        else:
            return f"❌ Failed to find {filename} after download"
            
    except Exception as e:
        return f"❌ Error downloading from Snowflake: {str(e)}"