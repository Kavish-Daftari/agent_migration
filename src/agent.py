from dotenv import load_dotenv
import os
from pathlib import Path
import shutil
from typing import List, Optional

from dotenv import load_dotenv
load_dotenv()


from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, AgentType
from langchain_core.tools import Tool


import snowflake.connector
from google.cloud import storage
from src.tools.list_ws_files import list_workspace_files
from src.tools.get_info import get_file_info
from src.tools.rename_file import rename_file
from src.tools.delete_ws import delete_workspace_file
from src.tools.download_sf import download_file_from_snowflake
from src.tools.upload_gcs import upload_file_to_gcs
from src.tools.list_sf_files import list_snowflake_stage_files
from src.tools.read_text_file import read_text_file    

load_dotenv()
WORKSPACE_DIR = Path("./agent_workspace")
WORKSPACE_DIR.mkdir(exist_ok=True)






tools = [
    list_snowflake_stage_files,
    list_workspace_files,
    download_file_from_snowflake,
    rename_file,
    read_text_file,
    get_file_info,
    upload_file_to_gcs,
    delete_workspace_file
]
# LLM
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# Create agent
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.OPENAI_FUNCTIONS,  # works with function calling
    verbose=True
)





system_prompt = """You are a proactive file management agent that helps users transfer files from Snowflake to Google Cloud Storage.

Your capabilities:
1. List files available in Snowflake stage 
2. Download files from Snowflake stage to your workspace
3. List, rename, read, and get info about files in workspace
4. Upload files from workspace to Google Cloud Storage
5. Delete files from workspace

IMPORTANT BEHAVIOR:
- When a user mentions uploading files to Snowflake or wants to move files, ALWAYS start by listing the Snowflake stage files using list_snowflake_stage_files()
- Show the user what files are available and ask which ones they want to transfer
- Be proactive - don't ask for filenames if you can list them first
- For each file transfer: Download → Confirm → Upload to GCS → Confirm
- Always use your tools to perform actions rather than just providing instructions

Example workflow:
1. User: "I want to move files from Snowflake to Google Cloud"
2. You: Use list_snowflake_stage_files() to show available files
3. You: "I found these files in your Snowflake stage: [list]. Which ones would you like to transfer to Google Cloud?"
4. User specifies files
5. You: Download, then upload each file, providing status updates

Be helpful, proactive, and always use your available tools."""

# Create the agent graph
agent_graph = create_agent(
    model=llm,
    tools=tools,
    system_prompt=system_prompt
)

def run_agent(user_input: str):
    """Run the agent with user input."""
    try:
        messages = [HumanMessage(content=user_input)]
        result = agent_graph.invoke({"messages": messages})
        
        # Extract the final message from the agent
        if result and "messages" in result:
            final_message = result["messages"][-1]
            if hasattr(final_message, 'content'):
                return final_message.content
            else:
                return str(final_message)
        else:
            return "No response from agent"
    except Exception as e:
        return f"Error running agent: {str(e)}"

if __name__ == "__main__":
    print("🤖 File Management Agent Started!")
    print("💡 I can help you transfer files from Snowflake to Google Cloud Storage.")
    print("💡 Tell me about files you've uploaded to Snowflake and I'll handle the transfer!")
    print("💡 Type 'quit' to exit.\n")
    
    while True:
        user_input = input("User: ").strip()
        
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("👋 Goodbye!")
            break
        
        if not user_input:
            continue
        
        print("\n🤖 Agent:")
        response = run_agent(user_input)
        print(response)
        print("\n" + "="*50 + "\n")