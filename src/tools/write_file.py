from langchain.tools import tool

from tools.paths import resolve_work_path
from tools.text import prepare_file_content


@tool
def write_file(path: str, content: str) -> str:
    """
    Create or overwrite a UTF-8 text file in the working directory.

    Works for any text file (.js, .java, .py, etc.).
    'content' is the full file body with real newline characters between lines. Do not wrap it
    in the markdown fence, do not encode line breaks as the two-character sequence backslash-n.

    Args:
        path: The relative path of the file to create/overwrite (e.g., README.md).
        content: Full file body with real newlines, no markdown fence, no \n encoding.
    """
    if not path:
        return "Error: Path is required"
    
    content = prepare_file_content(content)

    try:
        file_path = resolve_work_path(path)
    except ValueError as e:
        return f"Error: Path escapes the working directory: {e}"
    
    try:
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, encoding="utf-8") as f:
            f.write(content)
    except Exception as e:
        return f"Error: Failed to write the file {path!r}: {e}"
    
    return f"File {path!r} written successfully"


