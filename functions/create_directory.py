from langchain.tools import tool
import os

SANDBOX_DIRECTORY = os.path.abspath("sandbox")

@tool(
    description="Creates a new directory at the specified path within the working directory."
)
def create_directory(directory_path: str) -> str:        
    abs_dir_path = os.path.abspath(os.path.join(SANDBOX_DIRECTORY, directory_path))

    if not abs_dir_path.startswith(SANDBOX_DIRECTORY):
        return f'Error: Cannot create "{directory_path}" as it is outside the permitted working directory'

    if os.path.exists(abs_dir_path):
        if os.path.isdir(abs_dir_path):
            return f'Error: Directory "{directory_path}" already exists.'
        else:
            return f'Error: Cannot create directory. A file with the name "{directory_path}" already exists.'

    try:
        os.makedirs(abs_dir_path)
        return f'Successfully created directory: "{directory_path}"'
    except Exception as e:
        return f"Error creating directory '{directory_path}': {e}"
