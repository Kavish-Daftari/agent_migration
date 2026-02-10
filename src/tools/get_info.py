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
def get_file_info(filename: str) -> str:
    """Get information about a file in the workspace."""
    file_path = WORKSPACE_DIR / filename
    
    if not file_path.exists():
        return f"❌ File {filename} not found in workspace"
    
    stat = file_path.stat()
    return f"File: {filename}\nSize: {stat.st_size} bytes\nModified: {stat.st_mtime}"