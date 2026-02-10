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
def list_workspace_files() -> str:
    """List all files in the agent workspace directory."""
    files = list(WORKSPACE_DIR.glob("*"))
    if not files:
        return "No files found in workspace"
    
    file_list = []
    for f in files:
        if f.is_file():
            size = f.stat().st_size
            file_list.append(f"{f.name} ({size} bytes)")
    
    return "Files in workspace:\n" + "\n".join(file_list)

