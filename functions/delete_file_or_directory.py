from langchain.tools import tool
import os
import shutil

SANDBOX_DIRECTORY = os.path.abspath("sandbox")


@tool(
    description="Deletes a file or directory (and its contents) at the specified path within the working directory (sandbox)."
)
def delete_path(path: str) -> str:
    """
    Deletes a specified file or recursively deletes a directory within the sandbox.
    """
    abs_path = os.path.abspath(os.path.join(SANDBOX_DIRECTORY, path))

    if not abs_path.startswith(SANDBOX_DIRECTORY):
        return f'Error: Cannot delete "{path}" as it is outside the permitted working directory'

    if abs_path == SANDBOX_DIRECTORY:
        return f"Error: Cannot delete the root working directory."

    if not os.path.exists(abs_path):
        return f'Error: Path not found: "{path}"'

    try:
        if os.path.isfile(abs_path) or os.path.islink(abs_path):
            os.remove(abs_path)
            return f'Successfully deleted file: "{path}"'
        elif os.path.isdir(abs_path):
            shutil.rmtree(abs_path)
            return f'Successfully deleted directory and all its contents: "{path}"'
        else:
            return f'Error: "{path}" is neither a file nor a directory.'

    except Exception as e:
        return f"Error deleting path '{path}': {e}"
