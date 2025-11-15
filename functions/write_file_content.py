import os
from langchain.tools import tool

SANDBOX_DIRECTORY = os.path.abspath("sandbox")


@tool(description="Write or overwrite the content of a file at the specified path.")
def write_file_content(file_path, content):
    abs_file_path = os.path.abspath(os.path.join(SANDBOX_DIRECTORY, file_path))

    if not abs_file_path.startswith(SANDBOX_DIRECTORY):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(abs_file_path):
        try:
            os.makedirs(os.path.dirname(abs_file_path), exist_ok=True)
        except:
            return f"Error: creating directory: {e}"
    if os.path.exists(abs_file_path) and os.path.isdir(abs_file_path):
        return f'Error: "{file_path}" is a directory, not a file'

    try:
        with open(abs_file_path, "w") as f:
            f.write(content)
        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )
    except Exception as e:
        return f"Error writing to file: {e}"
