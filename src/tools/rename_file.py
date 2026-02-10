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
def rename_file(old_name: str, new_name: str) -> str:
    """Rename a file in the workspace."""
    old_path = WORKSPACE_DIR / old_name
    new_path = WORKSPACE_DIR / new_name
    
    if not old_path.exists():
        return f"❌ File {old_name} not found in workspace"
    
    if new_path.exists():
        return f"❌ File {new_name} already exists in workspace"
    
    try:
        old_path.rename(new_path)
        return f"✅ Renamed {old_name} to {new_name}"
    except Exception as e:
        return f"❌ Error renaming file: {str(e)}"