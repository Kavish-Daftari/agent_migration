from dotenv import load_dotenv
import os
from pathlib import Path
from google.cloud import storage

load_dotenv()

def upload_file(local_path: str,gcs_path: str):
    bucket_name = os.getenv("GCS_BUCKET_NAME")
    
    client=storage.Client()
    bucket=client.bucket(bucket_name)
    blob=bucket.blob(gcs_path)
    blob.upload_from_filename(local_path)
    print(f"uploaded {local_path} to google cloud gs://{bucket_name}")

if __name__ == "__main__":

    upload_file("test_upload.txt","/Users/kavishdaftari/Desktop/agent_migration2/test_upload.txt")   