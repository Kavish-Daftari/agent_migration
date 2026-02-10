from dotenv import load_dotenv
import os
from pathlib import Path
import snowflake.connector

load_dotenv()

def upload_file_to_stage(local_file: Path):
    if not local_file.exists():
        raise FileNotFoundError(local_file)

    conn = snowflake.connector.connect(
        user=os.environ["SF_USER"],
        password=os.environ["SF_PASSWORD"],
        account=os.environ["SF_ACCOUNT"],
        warehouse=os.environ["SF_WAREHOUSE"],
        database=os.environ["SF_DATABASE"],
        schema=os.environ["SF_SCHEMA"],
    )

    cur = conn.cursor()
    try:
        put_sql = f"""
        PUT file://{local_file.as_posix()}
        @{os.environ['SF_STAGE']}
        AUTO_COMPRESS=FALSE
        """
        cur.execute(put_sql)
        result = cur.fetchall()
        return result
    finally:
        cur.close()
        conn.close()


if __name__ == "__main__":
    result = upload_file_to_stage(Path("Test1.docx"))
    print("Upload result:")
    for r in result:
        print(r)