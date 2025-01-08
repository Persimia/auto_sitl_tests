import shutil, os
from paths_and_constants import test_dir, temp_save_dir

def copy_param_file(original_param_file_path, param_file_path):
    # Copy the file
    try:
        shutil.copyfile(original_param_file_path, param_file_path)
        print(f"File copied successfully from {original_param_file_path} to {param_file_path}")
    except FileNotFoundError:
        print(f"Error: The file at {original_param_file_path} does not exist.")
    except PermissionError:
        print("Error: Permission denied while copying the file.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def save_run_data(folder_name):
    save_dir_path = os.path.join(test_dir, folder_name)
    if os.path.exists(save_dir_path):
        print(f"Directory '{save_dir_path}' exists. Overwriting...")
        shutil.rmtree(save_dir_path)  # Remove the directory and its contents

    def ignore_func(directory, contents):
        if os.path.basename(directory) == "logs":
            for file in contents:
                if file == "LASTLOG.TXT":
                    with open(os.path.join(directory,file),"r") as f:
                        last_log = f.read().strip()
                        last_log = str(last_log).zfill(8) + '.BIN'
                        contents.remove(last_log)
                        return contents
        return []
            
    shutil.copytree(temp_save_dir, save_dir_path, ignore=ignore_func)
    
