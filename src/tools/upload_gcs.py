from dotenv import load_dotenv 
import os
from pathlib import Path 
import shutil
from typing import List,Optional 
from langchain_core.tools import tool
from google.cloud import storage
import snowflake.connector
load_dotenv()
WORKSPACE_DIR = Path("./agent_workspace")
WORKSPACE_DIR.mkdir(exist_ok=True)
@tool
def upload_file_to_gcs(filename: str) -> str:
    """Upload a file from workspace to Google Cloud Storage."""
    file_path = WORKSPACE_DIR / filename
    
    if not file_path.exists():
        return f"❌ File {filename} not found in workspace"
    
    try:
        bucket_name = os.environ["GCP_BUCKET_NAME"]
        client = storage.Client()
        bucket = client.bucket(bucket_name)
        
        blob = bucket.blob(filename)
        with open(file_path, "rb") as f:
            blob.upload_from_file(f)
        
        return f"✅ Uploaded {filename} to GCS: gs://{bucket_name}/{filename}"
    except Exception as e:
        return f"❌ Error uploading to GCS: {str(e)}"
