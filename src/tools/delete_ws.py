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
def delete_workspace_file(filename: str) -> str:
    """Delete a file from the workspace."""
    file_path = WORKSPACE_DIR / filename
    
    if not file_path.exists():
        return f"❌ File {filename} not found in workspace"
    
    try:
        file_path.unlink()
        return f"✅ Deleted {filename} from workspace"
    except Exception as e:
        return f"❌ Error deleting file: {str(e)}"