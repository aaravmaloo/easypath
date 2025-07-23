# <center> Documentation



```python

from easypath import *

create_folder("folder_path")  # Create a folder if it doesn't exist

create_folders(["folder1", "folder2"])  # Create multiple folders

remove_folder("folder_path", confirm=False)  # Recursively remove a folder with optional confirmation

remove_folders(["folder1", "folder2"])  # Remove multiple folders

list_folders("folder_path")  # List all subfolders in the given path

folder_exists("folder_path")  # Check if a folder exists

get_folder_size("folder_path")  # Get the size of a folder in bytes

copy_folder("src_folder", "dest_folder")  # Recursively copy a folder

move_folder("src_folder", "dest_folder")  # Move a folder to a new path

rename_folder("old_name", "new_name")  # Rename a folder

get_folder_info("folder_path")  # Get name, size, existence, and subfolders of a folder


touch_file("file.txt")  # Create or update a file’s modification time

remove_file("file.txt")  # Delete a file

file_exists("file.txt")  # Check if a file exists

rename_file("old.txt", "new.txt")  # Rename a file

move_file("file.txt", "backup/file.txt")  # Move a file

copy_file("source.txt", "copy.txt")  # Copy a file

getfilesize("file.txt")  # Get size of a file in bytes

get_file_info("file.txt")  # Get name, size, and existence of a file

list_files("folder")  # List all files in a folder


currentdir()  # Get the current working directory

list_all()  # List both files and folders in the current directory

get_perms()  # Get read/write/execute permissions of the current working dir

set_perms("path", read=True, write=True, execute=False)  # Set permissions (cross-platform: chmod or icacls)
