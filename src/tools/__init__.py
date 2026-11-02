from tools.edit import edit_file
from tools.list_files import list_files
from tools.read import read_file
from tools.write import write_file

ALL_TOOLS =[
    write_file,
    edit_file,
    read_file,
    list_files
]

def tool_catalog() -> list[dict[str, str]]:
    """Name + Description of all tools"""
    return [{"name": tool.name, "description": tool.description} for tool in ALL_TOOLS]