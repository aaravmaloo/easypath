from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Iterator, Sequence
import csv
import json
import os
import platform
import shutil
import stat
import subprocess

PathLike = str | Path


def _to_path(path: PathLike) -> Path:
    return path if isinstance(path, Path) else Path(path)


@dataclass(frozen=True)
class FileInfo:
    name: str
    path: str
    size: int
    exists: bool
    extension: str
    stem: str


@dataclass(frozen=True)
class FolderInfo:
    name: str
    path: str
    size: int
    exists: bool
    file_count: int
    folder_count: int


def ensure_dir(path: PathLike, parents: bool = True, exist_ok: bool = True) -> Path:
    folder = _to_path(path)
    folder.mkdir(parents=parents, exist_ok=exist_ok)
    return folder


def ensure_parent_dir(path: PathLike, parents: bool = True, exist_ok: bool = True) -> Path:
    file_path = _to_path(path)
    if file_path.parent:
        file_path.parent.mkdir(parents=parents, exist_ok=exist_ok)
    return file_path.parent


def ensure_file(path: PathLike, exist_ok: bool = True, parents: bool = True) -> Path:
    file_path = _to_path(path)
    if parents:
        ensure_parent_dir(file_path)
    file_path.touch(exist_ok=exist_ok)
    return file_path


def read_text(path: PathLike, encoding: str = "utf-8", errors: str = "strict") -> str:
    return _to_path(path).read_text(encoding=encoding, errors=errors)


def write_text(
    path: PathLike,
    data: str,
    encoding: str = "utf-8",
    errors: str = "strict",
    newline: str | None = None,
    parents: bool = True,
) -> Path:
    file_path = _to_path(path)
    if parents:
        ensure_parent_dir(file_path)
    file_path.write_text(data, encoding=encoding, errors=errors, newline=newline)
    return file_path


def append_text(
    path: PathLike,
    data: str,
    encoding: str = "utf-8",
    errors: str = "strict",
    newline: str | None = None,
    parents: bool = True,
) -> Path:
    file_path = _to_path(path)
    if parents:
        ensure_parent_dir(file_path)
    with file_path.open("a", encoding=encoding, errors=errors, newline=newline) as handle:
        handle.write(data)
    return file_path


def read_bytes(path: PathLike) -> bytes:
    return _to_path(path).read_bytes()


def write_bytes(path: PathLike, data: bytes, parents: bool = True) -> Path:
    file_path = _to_path(path)
    if parents:
        ensure_parent_dir(file_path)
    file_path.write_bytes(data)
    return file_path


def append_bytes(path: PathLike, data: bytes, parents: bool = True) -> Path:
    file_path = _to_path(path)
    if parents:
        ensure_parent_dir(file_path)
    with file_path.open("ab") as handle:
        handle.write(data)
    return file_path


def read_lines(path: PathLike, encoding: str = "utf-8", errors: str = "strict") -> list[str]:
    return _to_path(path).read_text(encoding=encoding, errors=errors).splitlines()


def write_lines(
    path: PathLike,
    lines: Iterable[str],
    encoding: str = "utf-8",
    errors: str = "strict",
    newline: str | None = "\n",
    parents: bool = True,
) -> Path:
    data = "".join(f"{line}{newline}" for line in lines)
    return write_text(path, data, encoding=encoding, errors=errors, newline=None, parents=parents)


def create_folder(folder_path: PathLike) -> None:
    path = _to_path(folder_path)
    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)
        print(f"Folder created: {path}")
    else:
        print(f"Folder already exists: {path}")


def create_folders(folders: Sequence[PathLike]) -> None:
    for folder in folders:
        create_folder(folder)


def remove_folder(folder_path: PathLike, confirm: bool = True, force: bool = False, dry_run: bool = False) -> None:
    path = _to_path(folder_path)

    if not path.exists() or not path.is_dir():
        print(f"Folder does not exist or is not a directory: {path}")
        return

    if confirm and not force:
        file_count = count_files(path, recursive=True)
        folder_count = count_folders(path, recursive=True)
        print(
            f"[remove_folder] The folder '{path.name}' has {file_count} files and {folder_count} folders. Continue y/n:"
        )
        choice = input().strip().lower()
        if choice != "y":
            print("Operation cancelled.")
            return

    if dry_run:
        print(f"[dry_run] Folder would be removed: {path}")
        return

    for item in path.iterdir():
        if item.is_dir():
            remove_folder(item, confirm=False, force=True)
        else:
            item.unlink()

    path.rmdir()
    print(f"Folder removed: {path}")


def remove_folders(folders: Sequence[PathLike], confirm: bool = True, force: bool = False) -> None:
    for folder in folders:
        remove_folder(folder, confirm=confirm, force=force)


def empty_folder(folder_path: PathLike) -> None:
    path = _to_path(folder_path)
    if not path.exists() or not path.is_dir():
        print(f"Folder does not exist or is not a directory: {path}")
        return
    for item in path.iterdir():
        if item.is_dir():
            remove_folder(item, confirm=False, force=True)
        else:
            item.unlink()
    print(f"Folder emptied: {path}")


def list_folders(folder_path: PathLike, recursive: bool = False) -> list[str]:
    path = _to_path(folder_path)
    if path.exists() and path.is_dir():
        if recursive:
            return [f.name for f in path.rglob("*") if f.is_dir()]
        return [f.name for f in path.iterdir() if f.is_dir()]
    print(f"Path does not exist or is not a directory: {path}")
    return []


def list_folders_recursive(folder_path: PathLike) -> list[str]:
    return list_folders(folder_path, recursive=True)


def list_files(folder_path: PathLike, recursive: bool = False) -> list[str]:
    path = _to_path(folder_path)

    if not path.exists() or not path.is_dir():
        print(f"Path does not exist or is not a directory: {path}")
        return []

    if recursive:
        files = [f.name for f in path.rglob("*") if f.is_file()]
    else:
        files = [f.name for f in path.iterdir() if f.is_file()]
    print(f"Files in '{path}': {files}")
    return files


def list_files_recursive(folder_path: PathLike) -> list[str]:
    return list_files(folder_path, recursive=True)


def list_paths(
    folder_path: PathLike,
    recursive: bool = False,
    include_files: bool = True,
    include_dirs: bool = True,
) -> list[str]:
    path = _to_path(folder_path)
    if not path.exists() or not path.is_dir():
        print(f"Path does not exist or is not a directory: {path}")
        return []

    iterator: Iterator[Path]
    iterator = path.rglob("*") if recursive else path.iterdir()

    results: list[str] = []
    for item in iterator:
        if item.is_file() and include_files:
            results.append(item.name)
        if item.is_dir() and include_dirs:
            results.append(item.name)
    return results


def glob_paths(folder_path: PathLike, pattern: str) -> list[str]:
    path = _to_path(folder_path)
    if not path.exists() or not path.is_dir():
        print(f"Path does not exist or is not a directory: {path}")
        return []
    return [p.name for p in path.glob(pattern)]


def rglob_paths(folder_path: PathLike, pattern: str) -> list[str]:
    path = _to_path(folder_path)
    if not path.exists() or not path.is_dir():
        print(f"Path does not exist or is not a directory: {path}")
        return []
    return [p.name for p in path.rglob(pattern)]


def find_files_by_extension(folder_path: PathLike, extension: str) -> list[str]:
    ext = extension if extension.startswith(".") else f".{extension}"
    return [p.name for p in _to_path(folder_path).rglob(f"*{ext}") if p.is_file()]


def find_files_by_name(folder_path: PathLike, filename: str) -> list[str]:
    return [p.name for p in _to_path(folder_path).rglob(filename) if p.is_file()]


def folder_exists(folder_path: PathLike) -> bool:
    path = _to_path(folder_path)
    exists = path.exists() and path.is_dir()
    print(f"Folder exists: {exists} for path: {path}")
    return exists


def is_empty_dir(folder_path: PathLike) -> bool:
    path = _to_path(folder_path)
    if not path.exists() or not path.is_dir():
        print(f"Path does not exist or is not a directory: {path}")
        return False
    return not any(path.iterdir())


def count_files(folder_path: PathLike, recursive: bool = False) -> int:
    path = _to_path(folder_path)
    if not path.exists() or not path.is_dir():
        return 0
    iterator = path.rglob("*") if recursive else path.iterdir()
    return sum(1 for item in iterator if item.is_file())


def count_folders(folder_path: PathLike, recursive: bool = False) -> int:
    path = _to_path(folder_path)
    if not path.exists() or not path.is_dir():
        return 0
    iterator = path.rglob("*") if recursive else path.iterdir()
    return sum(1 for item in iterator if item.is_dir())


def count_entries(folder_path: PathLike, recursive: bool = False) -> int:
    path = _to_path(folder_path)
    if not path.exists() or not path.is_dir():
        return 0
    iterator = path.rglob("*") if recursive else path.iterdir()
    return sum(1 for _ in iterator)


def get_folder_size(folder_path: PathLike) -> int:
    path = _to_path(folder_path)
    if not path.exists() or not path.is_dir():
        print(f"Path does not exist or is not a directory: {path}")
        return 0

    total_size = sum(f.stat().st_size for f in path.rglob("*") if f.is_file())
    print(f"Total size of folder '{path}': {total_size} bytes")
    return total_size


def copy_folder(src: PathLike, dst: PathLike, overwrite: bool = False) -> None:
    src_path = _to_path(src)
    dst_path = _to_path(dst)

    if not src_path.exists() or not src_path.is_dir():
        print(f"Source folder does not exist or is not a directory: {src_path}")
        return

    if dst_path.exists() and not overwrite:
        print(f"Destination folder already exists: {dst_path}")
        return

    shutil.copytree(src_path, dst_path, dirs_exist_ok=overwrite)
    print(f"Folder copied from {src_path} to {dst_path}")


def move_folder(src: PathLike, dst: PathLike, overwrite: bool = False) -> None:
    src_path = _to_path(src)
    dst_path = _to_path(dst)

    if not src_path.exists() or not src_path.is_dir():
        print(f"Source folder does not exist or is not a directory: {src_path}")
        return

    if dst_path.exists() and not overwrite:
        print(f"Destination folder already exists: {dst_path}")
        return

    if dst_path.exists() and overwrite:
        remove_folder(dst_path, confirm=False, force=True)

    shutil.move(str(src_path), str(dst_path))
    print(f"Folder moved from {src_path} to {dst_path}")


def rename_folder(old_name: PathLike, new_name: PathLike) -> None:
    old_path = _to_path(old_name)
    new_path = _to_path(new_name)

    if not old_path.exists() or not old_path.is_dir():
        print(f"Folder to rename does not exist or is not a directory: {old_path}")
        return

    if new_path.exists():
        print(f"New folder name already exists: {new_path}")
        return

    old_path.rename(new_path)

    print(f"Folder renamed from {old_path} to {new_path}")


def get_folder_info(folder_path: PathLike) -> FolderInfo:
    path = _to_path(folder_path)

    if not path.exists() or not path.is_dir():
        print(f"Path does not exist or is not a directory: {path}")
        return FolderInfo("", str(path), 0, False, 0, 0)

    info = FolderInfo(
        name=path.name,
        path=str(path),
        size=get_folder_size(path),
        exists=True,
        file_count=count_files(path, recursive=True),
        folder_count=count_folders(path, recursive=True),
    )

    print(f"Folder info: {info}")
    return info


def touch_file(file_path: PathLike, exist_ok: bool = True, parents: bool = False) -> None:
    path = _to_path(file_path)
    if parents:
        ensure_parent_dir(path)
    path.touch(exist_ok=exist_ok)
    print(f"File touched: {path}")


def remove_file(file_path: PathLike, missing_ok: bool = False) -> None:
    path = _to_path(file_path)
    if path.exists() and path.is_file():
        path.unlink()
        print(f"File removed: {path}")
        return
    if not missing_ok:
        print(f"File does not exist or is not a file: {path}")


def file_exists(file_path: PathLike) -> bool:
    path = _to_path(file_path)
    exists = path.exists() and path.is_file()
    print(f"File exists: {exists} for path: {path}")
    return exists


def rename_file(old_name: PathLike, new_name: PathLike) -> None:
    old_path = _to_path(old_name)
    new_path = _to_path(new_name)

    if not old_path.exists() or not old_path.is_file():
        print(f"File to rename does not exist or is not a file: {old_path}")
        return

    if new_path.exists():
        print(f"New file name already exists: {new_path}")
        return

    old_path.rename(new_path)

    print(f"File renamed from {old_path} to {new_path}")


def move_file(src: PathLike, dst: PathLike, overwrite: bool = False) -> None:
    src_path = _to_path(src)
    dst_path = _to_path(dst)

    if not src_path.exists() or not src_path.is_file():
        print(f"Source file does not exist or is not a file: {src_path}")
        return

    if dst_path.exists() and not overwrite:
        print(f"Destination file already exists: {dst_path}")
        return

    if dst_path.exists() and overwrite:
        dst_path.unlink()

    shutil.move(str(src_path), str(dst_path))

    print(f"File moved from {src_path} to {dst_path}")


def getfilesize(file_path: PathLike) -> int:
    path = _to_path(file_path)

    if not path.exists() or not path.is_file():
        print(f"Path does not exist or is not a file: {path}")
        return 0

    size = path.stat().st_size
    print(f"Size of file '{path}': {size} bytes")
    return size


def get_file_info(file_path: PathLike) -> FileInfo:
    path = _to_path(file_path)

    if not path.exists() or not path.is_file():
        print(f"Path does not exist or is not a file: {path}")
        return FileInfo("", str(path), 0, False, "", "")

    info = FileInfo(
        name=path.name,
        path=str(path),
        size=getfilesize(path),
        exists=True,
        extension=path.suffix,
        stem=path.stem,
    )

    print(f"File info: {info}")
    return info


def copy_file(src: PathLike, dst: PathLike, overwrite: bool = False) -> None:
    src_path = _to_path(src)
    dst_path = _to_path(dst)

    if not src_path.exists() or not src_path.is_file():
        print(f"Source file does not exist or is not a file: {src_path}")
        return

    if dst_path.exists() and not overwrite:
        print(f"Destination file already exists: {dst_path}")
        return

    if dst_path.exists() and overwrite:
        dst_path.unlink()

    shutil.copy2(src_path, dst_path)

    print(f"File copied from {src_path} to {dst_path}")


def currentdir() -> str:
    current_dir = Path.cwd()
    print(f"Current working directory: {current_dir}")
    return str(current_dir)


def get_perms() -> dict:
    perms = {
        "read": os.access(os.getcwd(), os.R_OK),
        "write": os.access(os.getcwd(), os.W_OK),
        "execute": os.access(os.getcwd(), os.X_OK),
    }

    print(f"Current user permissions: {perms}")
    return perms


def set_perms(path: PathLike, read: bool = True, write: bool = True, execute: bool = False) -> None:
    target = _to_path(path)

    if not target.exists():
        print(f"Path does not exist: {target}")
        return

    system = platform.system()

    try:
        if system == "Windows":
            if not read and not write and not execute:
                cmd = ["icacls", str(target), "/deny", "everyone:(F)"]
            else:
                if read and write and execute:
                    perm = "F"
                elif read and write:
                    perm = "M"
                elif read:
                    perm = "R"
                elif write:
                    perm = "W"
                else:
                    perm = "R"
                subprocess.run(["icacls", str(target), "/remove:d", "everyone"], stdout=subprocess.DEVNULL)
                cmd = ["icacls", str(target), "/grant:r", f"everyone:({perm})"]

            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                raise PermissionError(result.stderr.strip())
            print(f"[Windows] Permissions set for {target}")

        else:
            mode = 0
            if read:
                mode |= stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH
            if write:
                mode |= stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH
            if execute:
                mode |= stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH
            os.chmod(target, mode)
            print(f"[POSIX] Permissions set for {target}: {oct(mode)}")

    except PermissionError as exc:
        print(f"Permission denied while setting permissions for {target}.\n   Error: {exc}")
        print("Please run as Administrator (Windows) or with sudo (Linux/macOS).")


def list_all() -> dict:
    current_path = Path.cwd()

    files = [f.name for f in current_path.iterdir() if f.is_file()]
    folders = [f.name for f in current_path.iterdir() if f.is_dir()]

    result = {"files": files, "folders": folders}

    print(f"Files: {files}, Folders: {folders}")
    return result


def get_extension(path: PathLike) -> str:
    return _to_path(path).suffix


def strip_extension(path: PathLike) -> str:
    return _to_path(path).with_suffix("").name


def change_extension(path: PathLike, new_extension: str) -> str:
    ext = new_extension if new_extension.startswith(".") else f".{new_extension}"
    return str(_to_path(path).with_suffix(ext))


def ensure_extension(path: PathLike, extension: str) -> str:
    ext = extension if extension.startswith(".") else f".{extension}"
    path_obj = _to_path(path)
    if path_obj.suffix != ext:
        return str(path_obj.with_suffix(ext))
    return str(path_obj)


def get_stem(path: PathLike) -> str:
    return _to_path(path).stem


def get_name(path: PathLike) -> str:
    return _to_path(path).name


def get_parent(path: PathLike) -> str:
    return str(_to_path(path).parent)


def get_drive(path: PathLike) -> str:
    return _to_path(path).drive


def path_join(*parts: PathLike) -> str:
    if not parts:
        return ""
    current = _to_path(parts[0])
    for part in parts[1:]:
        current = current / _to_path(part)
    return str(current)


def path_split(path: PathLike) -> tuple[str, str]:
    path_obj = _to_path(path)
    return str(path_obj.parent), path_obj.name


def split_ext(path: PathLike) -> tuple[str, str]:
    path_obj = _to_path(path)
    return path_obj.stem, path_obj.suffix


def path_parts(path: PathLike) -> tuple[str, ...]:
    return _to_path(path).parts


def absolute_path(path: PathLike) -> str:
    return str(_to_path(path).absolute())


def resolve_path(path: PathLike) -> str:
    return str(_to_path(path).resolve())


def expand_path(path: PathLike) -> str:
    return str(_to_path(path).expanduser())


def relative_path(path: PathLike, start: PathLike | None = None) -> str:
    base = _to_path(start) if start is not None else Path.cwd()
    return str(_to_path(path).relative_to(base))


def as_posix_path(path: PathLike) -> str:
    return _to_path(path).as_posix()


def as_uri(path: PathLike) -> str:
    return _to_path(path).resolve().as_uri()


def read_json(path: PathLike, encoding: str = "utf-8") -> dict:
    return json.loads(read_text(path, encoding=encoding))


def write_json(
    path: PathLike,
    data: dict,
    encoding: str = "utf-8",
    indent: int = 2,
    sort_keys: bool = True,
    parents: bool = True,
) -> Path:
    payload = json.dumps(data, indent=indent, sort_keys=sort_keys)
    return write_text(path, payload + "\n", encoding=encoding, parents=parents)


def read_csv(
    path: PathLike,
    encoding: str = "utf-8",
    delimiter: str = ",",
) -> list[dict[str, str]]:
    file_path = _to_path(path)
    with file_path.open(newline="", encoding=encoding) as handle:
        reader = csv.DictReader(handle, delimiter=delimiter)
        return list(reader)


def write_csv(
    path: PathLike,
    rows: Iterable[dict[str, str]],
    fieldnames: Sequence[str],
    encoding: str = "utf-8",
    delimiter: str = ",",
    parents: bool = True,
) -> Path:
    file_path = _to_path(path)
    if parents:
        ensure_parent_dir(file_path)
    with file_path.open("w", newline="", encoding=encoding) as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter=delimiter)
        writer.writeheader()
        writer.writerows(rows)
    return file_path


def get_disk_usage(path: PathLike) -> tuple[int, int, int]:
    usage = shutil.disk_usage(_to_path(path))
    return usage.total, usage.used, usage.free


def create_symlink(target: PathLike, link_path: PathLike, overwrite: bool = False) -> None:
    target_path = _to_path(target)
    link = _to_path(link_path)
    if link.exists() and overwrite:
        if link.is_dir():
            remove_folder(link, confirm=False, force=True)
        else:
            link.unlink()
    os.symlink(target_path, link)
    print(f"Symlink created: {link} -> {target_path}")


def read_dir_tree(folder_path: PathLike, max_depth: int = 2) -> list[str]:
    path = _to_path(folder_path)
    if not path.exists() or not path.is_dir():
        return []

    results: list[str] = []
    base_depth = len(path.parts)

    for item in path.rglob("*"):
        depth = len(item.parts) - base_depth
        if depth <= max_depth:
            results.append(str(item))
    return results
