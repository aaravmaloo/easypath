# <center> Documentation

```python
from easypath import *

# Folder operations
create_folder("folder_path")  # Create a folder if it doesn't exist
create_folders(["folder1", "folder2"])  # Create multiple folders
remove_folder("folder_path", confirm=False)  # Recursively remove a folder
remove_folders(["folder1", "folder2"], confirm=False)  # Remove multiple folders
empty_folder("folder_path")  # Empty a folder without deleting it
list_folders("folder_path")  # List subfolders
list_folders_recursive("folder_path")  # Recursive folder listing
folder_exists("folder_path")  # Check if a folder exists
is_empty_dir("folder_path")  # Check if a folder is empty
count_files("folder_path", recursive=True)  # Count files
count_folders("folder_path", recursive=True)  # Count folders
count_entries("folder_path", recursive=True)  # Count all entries
get_folder_size("folder_path")  # Folder size in bytes
get_folder_info("folder_path")  # FolderInfo dataclass
copy_folder("src_folder", "dest_folder", overwrite=True)  # Copy a folder
move_folder("src_folder", "dest_folder", overwrite=True)  # Move a folder
rename_folder("old_name", "new_name")  # Rename a folder

# File operations
touch_file("file.txt", parents=True)  # Create or update a file’s modification time
remove_file("file.txt", missing_ok=True)  # Delete a file
file_exists("file.txt")  # Check if a file exists
rename_file("old.txt", "new.txt")  # Rename a file
move_file("file.txt", "backup/file.txt", overwrite=True)  # Move a file
copy_file("source.txt", "copy.txt", overwrite=True)  # Copy a file
getfilesize("file.txt")  # Get size of a file in bytes
get_file_info("file.txt")  # FileInfo dataclass
list_files("folder")  # List all files in a folder
list_files_recursive("folder")  # List files recursively

# Reading/writing
read_text("notes.txt")
write_text("notes.txt", "Hello")
append_text("notes.txt", "World")
read_bytes("image.png")
write_bytes("out.bin", b"data")
append_bytes("out.bin", b"more")
read_lines("notes.txt")
write_lines("notes.txt", ["a", "b", "c"])
read_json("config.json")
write_json("config.json", {"debug": True})
read_csv("data.csv")
write_csv("data.csv", [{"name": "A"}], fieldnames=["name"])

# Path utilities
path_join("home", "user", "file.txt")
path_split("/tmp/file.txt")
split_ext("/tmp/file.txt")
path_parts("/tmp/file.txt")
absolute_path(".")
resolve_path(".")
expand_path("~/file.txt")
relative_path("/tmp/file.txt", start="/tmp")
as_posix_path("C:\\Temp\\file.txt")
as_uri("/tmp/file.txt")
get_extension("/tmp/file.txt")
strip_extension("/tmp/file.txt")
change_extension("/tmp/file.txt", "md")
ensure_extension("/tmp/file", "txt")
get_stem("/tmp/file.txt")
get_name("/tmp/file.txt")
get_parent("/tmp/file.txt")
get_drive("C:\\Temp\\file.txt")

# Search helpers
glob_paths("/tmp", "*.txt")
rglob_paths("/tmp", "*.txt")
find_files_by_extension("/tmp", "txt")
find_files_by_name("/tmp", "notes.txt")
list_paths("/tmp", recursive=True)

# System helpers
currentdir()  # Current working directory
list_all()  # List both files and folders in the current directory
get_perms()  # Read/write/execute permissions of the current working dir
set_perms("path", read=True, write=True, execute=False)  # Set permissions
get_disk_usage("/")  # Disk usage in bytes
create_symlink("target", "link", overwrite=True)  # Create a symlink
read_dir_tree("/tmp", max_depth=2)  # Simple directory tree listing
```
