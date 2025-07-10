import os
from functions.config import MAX_CHARS
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the content of a file in the specified path, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to file to be read, relative to the working directory.",
            ),
        },
    ),
)

def get_file_content(working_directory, file_path):
    try:
        abs_working_dir = os.path.abspath(working_directory)
        target_file_path = os.path.join(working_directory, file_path)
        abs_target_file_path = os.path.abspath(target_file_path)
        if abs_working_dir not in abs_target_file_path:
            return(f'Error: Cannot list "{file_path}" as it is outside the permitted working directory')
        if not os.path.isfile(target_file_path):
            return (f'Error: "{file_path}" is not a file')

        with open(target_file_path, "r") as f:
            file_content_string = f.read()
    except Exception as e:
        return f"Error: {e}"
    
    if len(file_content_string) > MAX_CHARS:
        file_content_string =  file_content_string[:MAX_CHARS - 1] + f"\n[...File {file_path} truncated at 10000 characters]"
    return file_content_string