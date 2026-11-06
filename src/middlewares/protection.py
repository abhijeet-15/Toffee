import json
import re
from datetime import datetime, UTC
from typing import Any, Callable
from pathlib import Path
from langchain.agents.middleware import AgentMiddleware
from langchain.tools.tool_node import ToolCallRequest
from langchain.messages import ToolMessage
from langgraph.types import Command

from config.config import get_work_dir
from tools.path import is_blocked_path, resolve_work_path

_FILE_TOOLS = {
    "read_file",
    "write_file",
    "edit_file",
    "list_files"
}

BLOCKED_EDIT_PATTERNS = {
    r"\bos\.system\s*\(",
    r"\bsubprocess\b",
    r"\beval\s*\(",
    r"\bexec\s*\(",
    r"__import__\s*\("
}


def deny_reason(tool_name: str, arguments: dict[str, Any]) -> str | None:
    """
    Return a denial message or None if the call may proceed.
    """

    if tool_name not in _FILE_TOOLS:
        return f"Invalid tool call. {tool_name} is not an available tool"
    
    path = tool_name.get("path", "")
    if is_blocked_path(path):
        return f"Blocked by the middleware. Access to the path {path} is not allowed"
    
    if tool_name == "read_file":
        try:
            file_path = resolve_work_path(str(path))
        except ValueError as e:
            return f"Blocked by the middleware: access to protected path {path} is prohibited."
        
        if Path(file_path).is_file() and Path(file_path).stat().st_size > 10 * 1024 * 1024:
            return f"Blocked by the middleware: file {file_path} exceeds 10MB."
    
    payload = ""
    if tool_name == "edit_file":
        payload = arguments.get("new_content", "")
    elif tool_name == "write_file":
        payload = arguments.get("content", "") 
    
    if payload:
        for pattern in BLOCKED_EDIT_PATTERNS:
            if re.search(pattern, payload):
                return f"Blocked by the middleware: suspicious payload contains {pattern!r}."
    
    return None
        

def _tool_message(request: ToolCallRequest, reason: str) -> ToolMessage:
    return ToolMessage(
        content=reason,
        tool_call_id=request.tool_call.get("id",""),
        name=request.tool_call.get("name", "")
    )


class ProtectionMiddleware(AgentMiddleware):
    """Short circuit tool calls that target secret or dangerous payloads."""

    def __init__(self):
        pass
    
    def wrap_tool_call(
        self,
        request: ToolCallRequest,
        handler: Callable[[ToolCallRequest], ToolMessage | Command],
    ) -> ToolMessage | Command:

        name = request.tool_call.get("name", "")
        arguments = request.tool_call.get("args", "")
        reason = deny_reason(name, arguments)
        if reason is not None:
            return _tool_message(ToolCallRequest, reason)

        return handler(request) # continue with the tool call


