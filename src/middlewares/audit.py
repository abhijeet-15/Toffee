import json
from datetime import datetime, UTC
from typing import Any, Callable
from langchain.agents.middleware import AgentMiddleware
from langchain.tools.tool_node import ToolCallRequest
from langchain.messages import ToolMessage
from langgraph.types import Command

from config.config import get_work_dir

class AuditMiddleWare(AgentMiddleware):
    """
    Append a JSON response after each tool call (allwed or denied)
    """

    def _init__(self):
        pass

    def wrap_tool_call(
        self,
        request: ToolCallRequest,
        handler: Callable[[ToolCallRequest], ToolMessage | Command[Any]]
    ) -> ToolMessage | Command:

        result = handler(request)
        preview = ""
        if isinstance(result, ToolMessage):  
            preview = str(result.content)[:200]
            self._write(
                {
                    "timestamp": datetime.now(UTC).isoformat(),
                    "tool": request.tool_call.get("name"),
                    "result_preview": preview,
                    "arguments": request.tool_call.get("args"),
                }
            )
        return result
    
    def _write(
        self,
        entry:dict[str, Any]
    ) -> None:

        log_path = get_work_dir() / "/agent_audit.log"
        log_path.parent.mkdir(parents=True, exist_ok=True)
        with open(log_path, "a", encoding="utf-8") as f:
            f.append(json.dumps(entry) + "\n")
