from dotenv import load_dotenv 
import os
from pathlib import Path 
import shutil
from typing import List,Optional 
from langchain_core.tools import tool
import snowflake.connector
load_dotenv()

@tool
def list_snowflake_stage_files() -> str:
    """List all files available in the Snowflake stage."""
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
        
        # List files in stage
        cur.execute(f"LIST @{stage}")
        result = cur.fetchall()
        
        cur.close()
        conn.close()
        
        if not result:
            return "No files found in Snowflake stage"
        
        file_list = []
        for row in result:
            # Snowflake LIST returns: name, size, md5, last_modified
            filename = row[0].split('/')[-1]  # Get just the filename
            size_bytes = row[1]
            file_list.append(f"📄 {filename} ({size_bytes} bytes)")
        
        return "Files available in Snowflake stage:\n" + "\n".join(file_list)
        
    except Exception as e:
        return f"❌ Error listing Snowflake stage files: {str(e)}"
 
    

