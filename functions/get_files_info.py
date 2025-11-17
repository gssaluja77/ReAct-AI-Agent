import os
from langchain.tools import tool

SANDBOX_DIRECTORY = os.path.abspath("sandbox")

@tool(
    description="Lists files in the specified directory along with their sizes, constrained to the working directory."
)
def get_files_info(directory="."):
    target_dir = os.path.abspath(os.path.join(SANDBOX_DIRECTORY, directory))

    try:
        if os.path.commonpath([SANDBOX_DIRECTORY, target_dir]) != SANDBOX_DIRECTORY:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    except ValueError:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    if not os.path.exists(target_dir):
        return f'Error: "{directory}" does not exist'
    if not os.path.isdir(target_dir):
        return f'Error: "{directory}" is not a directory'

    def get_dir_size(path):
        total = 0
        try:
            for entry in os.scandir(path):
                try:
                    if entry.is_symlink():
                        continue
                    if entry.is_file(follow_symlinks=False):
                        try:
                            total += entry.stat(follow_symlinks=False).st_size
                        except (OSError, PermissionError):
                            continue
                    elif entry.is_dir(follow_symlinks=False):
                        total += get_dir_size(entry.path)
                except (OSError, PermissionError):
                    continue
        except (OSError, PermissionError):
            pass
        return total

    lines = []
    try:
        for filename in sorted(os.listdir(target_dir)):
            filepath = os.path.join(target_dir, filename)
            is_dir = os.path.isdir(filepath)
            try:
                if is_dir:
                    size = get_dir_size(filepath)
                else:
                    try:
                        size = os.path.getsize(filepath)
                    except (OSError, PermissionError):
                        size = 0
            except Exception:
                size = 0

            lines.append(f"- {filename}: file_size={size} bytes, is_dir={is_dir}")
    except Exception as e:
        return f"Error listing files: {e}"

    return "\n".join(lines)
