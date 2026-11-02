import json
import os
from pathlib import Path

from langchain_core.tools import tool

from config.config import get_work_dir
from tools.paths import resolve_work_path


@tool
def list_files(path: str = ".") -> str:
    """
    List files and directories under a given path in the working directory.

    Args:
        path: Relative directory to the list. Default to the workig directory root.
    """

    work_dir = get_work_dir()

    try:
        base_path = resolve_work_path(path)
    except ValueError:
        return json.dumps({"error": f"Path {path!r} escapes working directory"})   
    
    if not base_path.exists():
        return json.dumps({"error": f"Path {path!r} does not exits"})
    
    if not base_path.is_dir():
        return json.dumps({"error": f"Path {path!r} is not a directory"})
    
    result: list[str] = []

    for dirpath, dirnames, filenames in os.walk(base_path):
        root_path = Path(dirpath)
        rel_root = root_path.relative_to(work_dir)

        for dir_names in sorted(dirnames):
            result.append(f"{(rel_root / dir_names).as_posix()}/")
        for file_name in sorted(filenames):
            result.append(f"{(rel_root / file_name).as_posix()}")

    return json.dumps(result)


