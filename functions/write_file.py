import os
from google.genai import types


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a given file path, contrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file_path to file, relative to the working directory, to which the content is written.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content which will be written to the file.",
            ),
        },
    ),
)

def write_file(working_directory, file_path, content):
    abs_working_dir = os.path.abspath(working_directory)
    target_file_path = os.path.join(working_directory, file_path)
    abs_target_file_path = os.path.abspath(target_file_path)
    if abs_working_dir not in abs_target_file_path:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    try:
        target_directory = os.path.dirname(target_file_path)
        if not os.path.exists(target_directory):
            os.makedirs(os.path.dirname(target_directory))
        
        with open(target_file_path, "w") as f:
            f.write(content)
    except Exception as e:
        return f"Error: {e}"

    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'