import os

def get_files_info(working_directory, directory=None):
    try:
        abs_working_dir = os.path.abspath(working_directory)
        abs_target_dir = os.path.join(working_directory, directory)
        if abs_working_dir not in os.path.abspath(abs_target_dir):
            return(f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
        if not os.path.isdir(abs_target_dir):
            return (f'Error: "{directory}" is not a directory')
        
        files_info = []
        for dir in os.listdir(abs_target_dir):
            path = os.path.join(abs_target_dir, dir)
            files_info.append(f"- {dir}: file_size={os.path.getsize(path)}, is_dir={os.path.isdir(path)}")
    except Exception as e:
        return (f'Error: {e}') 
    return "\n".join(files_info) 
