from pathlib import Path

from langchain_core.tools import tool

from tools.paths import resolve_work_path


@tool
def read_file(path: str) -> str:
    """
    Reads a UTF-8 encoded file from the working directory.

    Args:
        path: Relative path of the file, e.g. 'src/index.py' or 'README.md' or 'data/example.json.'
    """

    try:
        file_path = resolve_work_path(path)
    except ValueError as e:
        raise ValueError(f"Path escapes working directory: {e}")

    try:
        read_content = Path(file_path).read_text(encoding="utf-8")
        return read_content
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    except PermissionError:
        raise PermissionError(f"Permission denied: {file_path}")
    except OSError as e:
        raise RuntimeError(f"Error reading the file: {e}")
    except Exception as e:
        raise Exception(f"Error reading the file: {e}")
