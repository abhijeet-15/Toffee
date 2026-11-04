from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware

from tools.write_file import write_file

def build_hitl_middleware() -> HumanInTheLoopMiddleware:
    return HumanInTheLoopMiddleware(
        interrupt_on={
            "write_file": {
                "allowed_decisions": ["approve", "edit", "reject"],
                "description": "Write or override a file on the disk"
            },
            "edit_file": {
                "allowed_decisions": ["approve", "edit", "reject"],
                "description": "Edit an existing file on the disk"
            }
            "read_file": False,
            "list_files": False
        },
        description_prefix="Coding agent needs your approval to move ahead"
    )

