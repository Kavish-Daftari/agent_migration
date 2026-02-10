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
def read_text_file(filename: str) -> str:
    """Read the contents of a text file in the workspace."""
    file_path = WORKSPACE_DIR / filename
    
    if not file_path.exists():
        return f"❌ File {filename} not found in workspace"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Truncate if too long
        if len(content) > 2000:
            content = content[:2000] + "\n... (truncated)"
        
        return f"Content of {filename}:\n{content}"
    except Exception as e:
        return f"❌ Error reading file: {str(e)}"