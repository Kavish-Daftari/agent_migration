from dotenv import load_dotenv
import os
from pathlib import Path
import snowflake.connector

load_dotenv()

def download_file_from_stage(filename: str, out_dir: Path):
    out_dir.mkdir(parents=True, exist_ok=True)

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
    try:
        # GET pulls file from stage to local folder
        cur.execute(f"GET @{stage}/{filename} file://{out_dir.as_posix()}")
        result = cur.fetchall()
        return result
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    filename = "test_upload.txt"  # must match exactly what you uploaded
    out_dir = Path("./workspace_download")

    result = download_file_from_stage(filename, out_dir)

    print("GET result:")
    for r in result:
        print(r)

    # Snowflake sometimes downloads into nested folders, so search for the file
    matches = list(out_dir.rglob(filename))
    print("\nDownloaded file paths found:")
    for m in matches:
        print(m)