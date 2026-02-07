# <center> easypath
## <center> PathLib simplified to its most.
**easypath** is a lightweight Python utility module that simplifies common file and folder path operations using Python’s built-in `pathlib` library.

## Why use easypath?

Working with files and directories in Python can often involve repetitive and verbose code. `easypath` wraps the most frequently used operations into simple functions to help make your scripts cleaner, easier to read, and quicker to write.

## Features

- Create folders if they don’t exist
- Delete folders or files
- Check if a path exists
- Read and write text or binary files
- Join paths easily across platforms
- List files or directories
- Get file names, extensions, and more

## New additions (50+ utilities)

1. `PathLike` type alias for `str | Path`
2. `_to_path` internal helper for safe conversion
3. `FileInfo` dataclass for file metadata
4. `FolderInfo` dataclass for folder metadata
5. `ensure_dir` directory creation helper
6. `ensure_parent_dir` parent directory creation helper
7. `ensure_file` file creation helper
8. `read_text` text file reader
9. `write_text` text file writer
10. `append_text` text file appender
11. `read_bytes` binary file reader
12. `write_bytes` binary file writer
13. `append_bytes` binary file appender
14. `read_lines` read file into line list
15. `write_lines` write iterable of lines
16. `remove_folder` with `confirm`, `force`, and `dry_run`
17. `remove_folders` with confirmation control
18. `empty_folder` delete folder contents only
19. `list_folders` optional recursive mode
20. `list_folders_recursive` convenience wrapper
21. `list_files` optional recursive mode
22. `list_files_recursive` convenience wrapper
23. `list_paths` mixed file/folder listing
24. `glob_paths` glob matcher
25. `rglob_paths` recursive glob matcher
26. `find_files_by_extension` recursive extension search
27. `find_files_by_name` recursive name search
28. `is_empty_dir` directory emptiness check
29. `count_files` file counter
30. `count_folders` folder counter
31. `count_entries` total entry counter
32. `copy_folder` with overwrite support
33. `move_folder` with overwrite support
34. `get_folder_info` returns a `FolderInfo`
35. `touch_file` with parent creation
36. `remove_file` with `missing_ok`
37. `move_file` with overwrite support
38. `copy_file` with overwrite support
39. `get_file_info` returns a `FileInfo`
40. `get_extension` file extension helper
41. `strip_extension` remove file extension
42. `change_extension` replace file extension
43. `ensure_extension` enforce file extension
44. `get_stem` stem (filename without suffix)
45. `get_name` filename helper
46. `get_parent` parent folder helper
47. `get_drive` drive letter helper
48. `path_join` cross-platform path join
49. `path_split` split into parent + name
50. `split_ext` split into stem + suffix
51. `path_parts` tuple of path parts
52. `absolute_path` absolute path conversion
53. `resolve_path` resolve symlinks + absolute
54. `expand_path` expand `~` user paths
55. `relative_path` relative path builder
56. `as_posix_path` convert to POSIX string
57. `as_uri` convert to `file://` URI
58. `read_json` JSON loader
59. `write_json` JSON writer
60. `read_csv` CSV reader
61. `write_csv` CSV writer
62. `get_disk_usage` disk usage helper
63. `create_symlink` symlink creation helper
64. `read_dir_tree` simple directory tree reader

## Installation

This module has no external dependencies. You can simply copy it into your project or install it manually once published.

```bash
pip install easypath
```
