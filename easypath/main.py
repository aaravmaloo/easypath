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