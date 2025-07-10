import os
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

def get_files_info(working_directory, directory=None):
    try:
        target_dir = os.path.join(working_directory, directory)
        if os.path.abspath(working_directory) not in os.path.abspath(target_dir):
            return(f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
        if not os.path.isdir(target_dir):
            return (f'Error: "{directory}" is not a directory')
        
        files_info = []
        for dir in os.listdir(target_dir):
            path = os.path.join(target_dir, dir)
            files_info.append(f"- {dir}: file_size={os.path.getsize(path)}, is_dir={os.path.isdir(path)}")
    except Exception as e:
        return (f'Error: {e}') 
    return "\n".join(files_info) 
