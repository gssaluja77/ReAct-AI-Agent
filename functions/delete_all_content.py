import os
import shutil

SANDBOX_DIRECTORY = os.path.abspath("sandbox")


def delete_path(file_path: str) -> str:
    """
    Deletes a file or directory at the specified path.
    Returns a success or error message.
    """
    abs_path = os.path.abspath(os.path.join(SANDBOX_DIRECTORY, file_path))

    if not os.path.exists(abs_path):
        return f"Error: File or directory not found: {file_path}"

    if os.path.isfile(abs_path):
        try:
            os.remove(abs_path)
            return f"Successfully deleted file: {file_path}"
        except Exception as e:
            return f"Error deleting file {file_path}: {str(e)}"

    elif os.path.isdir(abs_path):
        try:
            shutil.rmtree(abs_path)
            return f"Successfully deleted directory: {file_path}"
        except Exception as e:
            return f"Error deleting directory {file_path}: {str(e)}"

    else:
        return f"Error: {file_path} is not a file or directory."


def delete_all_content_in_directory(directory_path: str) -> str:
    """
    Deletes all content (files and subdirectories) within the specified directory.
    Returns a success or error message.
    """
    abs_path = os.path.abspath(os.path.join(SANDBOX_DIRECTORY, directory_path))

    if not abs_path.startswith(SANDBOX_DIRECTORY):
        return f"Error: Cannot delete '{directory_path}' as it is outside the sandbox directory."

    if not os.path.isdir(abs_path):
        return f"Error: '{directory_path}' is not a directory."

    try:
        for item in os.listdir(abs_path):
            item_path = os.path.join(directory_path, item)
            result = delete_path(item_path)
            if "Error" in result:
                return result
        return f"Successfully deleted all content in directory: '{directory_path}'"
    except Exception as e:
        return f"Error deleting content in directory '{directory_path}': {str(e)}"
