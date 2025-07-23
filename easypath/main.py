from pathlib import Path




def create_folder(folder_path: str) -> None:
    """
    Create a folder if it does not exist.

    :param folder_path: Path to the folder to be created.
    """
    path = Path(folder_path)
    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)
        print(f"Folder created: {path}")
    else:
        print(f"Folder already exists: {path}")


def create_folders(folders: list) -> None:
    """
    Create multiple folders if they do not exist.

    :param folders: List of folder paths to be created.
    """
    for folder in folders:
        create_folder(folder)


def remove_folder(folder_path: str) -> None:
    """
    Remove a folder recursively if it exists, even if it is not empty.

    :param folder_path: Path to the folder to be removed.
    """
    path = Path(folder_path)
    
    if not path.exists() or not path.is_dir():
        print(f"Folder does not exist or is not a directory: {path}")
        return

    file_count = sum(1 for _ in path.glob('**/*') if _.is_file())
    folder_count = sum(1 for _ in path.glob('**/*') if _.is_dir())

    print(f"[delete_folder] The folder '{path.name}' has {file_count} files and {folder_count} folders. Continue y/n:")
    choice = input().strip().lower()

    if choice != 'y':
        print("Operation cancelled.")
        return

    for item in path.iterdir():
        if item.is_dir():
            remove_folder(item)
        else:
            item.unlink()

    path.rmdir()
    print(f"Folder removed: {path}")

def remove_folders(folders: list) -> None:
    """
    Remove multiple folders if they exist.

    :param folders: List of folder paths to be removed.
    """
    for folder in folders:
        remove_folder(folder)



def list_folders(folder_path: str) -> list:
    """
    List all folders in a given path.

    :param folder_path: Path to the directory to list folders from.
    :return: List of folder names in the specified path.
    """
    path = Path(folder_path)
    if path.exists() and path.is_dir():
        return [f.name for f in path.iterdir() if f.is_dir()]
    else:
        print(f"Path does not exist or is not a directory: {path}")
        return []
    


def folder_exists(folder_path: str) -> bool:
    """
    Check if a folder exists.

    :param folder_path: Path to the folder to check.
    :return: True if the folder exists, False otherwise.
    """
    path = Path(folder_path)
    exists = path.exists() and path.is_dir()
    print(f"Folder exists: {exists} for path: {path}")
    return exists


def get_folder_size(folder_path: str) -> int:
    """
    Get the size of a folder in bytes.

    :param folder_path: Path to the folder.
    :return: Size of the folder in bytes.
    """
    path = Path(folder_path)
    if not path.exists() or not path.is_dir():
        print(f"Path does not exist or is not a directory: {path}")
        return 0
    
    total_size = sum(f.stat().st_size for f in path.glob('**/*') if f.is_file())
    print(f"Total size of folder '{path}': {total_size} bytes")
    return total_size


