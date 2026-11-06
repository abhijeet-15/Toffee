from langchain.tools import tool

from tools.paths import resolve_work_path
from tools.text import prepare_file_content


@tool
def edit_file(path: str, old_content: str, new_content: str) -> str:
    """
    Replace `old_content` with `new_content` in the file at path `path`

    Language agnostic: .js, .java, .py and other text files all use exact substring replace.
    Pass an empty `old_content` to create new files(same as `write_file`).
    Both strings must use real newlines, and not the two-character sequence backslash-n.

    Args:
        path: Relative path of the file to edit (e.g. "README.md")
        old_content: Exact text to replace. Empty string creates new file.
        new_content: Exact text to replace with.
    """

    if not path or old_content == new_content:
        return "Error: Invalid input"
    
    old_content = prepare_file_content(old_content)
    new_content = prepare_file_content(new_content)
    try:
        file_path = resolve_work_path(path)
    except ValueError as e:
        return f"Error: Path escapes the working directory: {e}"
    
    try:
        if old_content == "":
            file_path.parent.mkdir(parent=True, exist_ok=True)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(new_content)
        return f"Created new file {path}"

    except Exception as e:
        return f"Error: Failed to write the file {path!r}: {e}" 
    
    try:
        old_str = file_path.read_text(encoding="utf-8")
    except Exception as e:
        return f"Error: Failed to read the file {path!r}: {e}" 
    
    if old_content not in old_str:
        return f"Error: {path!r} does not contain {old_content!r}"
    
    try:
        new_str = old_str.replace(old_content, new_content)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_str)
    except Exception as e:
        return f"Error: Failed to read the file {path!r}: {e}" 
    
    return f"Replaced {old_content!r} with {new_content!r} in {path!r}"
