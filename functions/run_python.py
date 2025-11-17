import os
import subprocess
from langchain.tools import tool

SANDBOX_DIRECTORY = os.path.abspath("sandbox")

@tool(
    description="Executes a Python file within the working directory and returns the output from the interpreter.",
    args_schema={
        "type": "object",
        "properties": {
            "file_path": {"type": "string", "description": "Python file to execute"},
            "args": {
                "type": "array",
                "items": {"type": "string"},
                "description": "List of arguments",
            },
        },
        "required": ["file_path"],
    },
)
def run_python_file(file_path, args=[]):
    abs_file_path = os.path.abspath(os.path.join(SANDBOX_DIRECTORY, file_path))

    if not abs_file_path.startswith(SANDBOX_DIRECTORY):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(abs_file_path):
        return f'Error: File "{file_path}" not found.'
    if not abs_file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    try:
        commands = ["python", abs_file_path]
        if args:
            commands.extend(args)

        res = subprocess.run(
            commands, timeout=30, capture_output=True, text=True, cwd=SANDBOX_DIRECTORY
        )
        output = []
        if res.stdout:
            output.append(f"STDOUT:\n{res.stdout}")
        if res.stderr:
            output.append(f"STDERR:\n{res.stderr}")
        if res.returncode != 0:
            output.append(f"Process exited with code {res.returncode}")

        return "\n".join(output) if output else "No output produced."
    except Exception as e:
        return f"Error: executing Python file: {e}"
