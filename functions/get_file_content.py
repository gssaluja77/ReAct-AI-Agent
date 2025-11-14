from langchain.tools import tool
import os
from config import CHARACTER_LIMIT

SANDBOX_DIRECTORY = os.path.abspath("sandbox")

@tool(description=f"Reads and returns the first {CHARACTER_LIMIT} characters of the content from a specified file within the working directory.")
def get_file_content(file_path: str) -> str:
    abs_file_path = os.path.abspath(os.path.join(SANDBOX_DIRECTORY, file_path))

    if not abs_file_path.startswith(SANDBOX_DIRECTORY):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(abs_file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    try:
        with open(abs_file_path, "r") as f:
            file_data = f.read(CHARACTER_LIMIT)
            if os.path.getsize(abs_file_path) > CHARACTER_LIMIT:
                file_data = file_data.strip() + f"...File '{file_path}' truncated at {CHARACTER_LIMIT} characters."
        return file_data
    except Exception as e:
        return f"Error reading file '{file_path}': {e}"
    