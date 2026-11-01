from typing import Any

from langchain.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage


def user_input(text: str) -> str:
    """OpenAI format dict for user input """
    return {"role": "user", "content": text}

def last_ai_text(messages: list[Any]) -> str:
    """
    Last AI message content
    """
    for message in reversed(messages):
        if not isinstance(message, AIMessage):
            continue
        if getattr(message, "tool_calls", None):
            continue
        content = message.content
        if isinstance(content, str):
            return content
        if isinstance(content, list):
            parts = [
                block.get("text", "") for block in content if isinstance(block, dict) and block.get("type") == "text"
            ]
            return "\n".join(part for part in parts if parts)

def last_tool_text(messages: list[Any]) -> str:
    """
    Returns the content of the last tool result - useful when the model skips a chat reply
    """
    for message in reversed(messages):
        if isinstance(message, ToolMessage):
            content = message.content
            return content if isinstance(content, str) else str(content)
    return ""

def describe_message(message) -> str:
    """
    Useful for logging and debugging
    """
    role = type(message).__name__.replace("Message", "").lower() + " "
    content = message.content
    preview = content if isinstance(content, str) else str(content)
    preview = preview.replace("\n", "")
    extra = ""

    if isinstance(message, AIMessage) and message.tool_calls:
        names = ",".join(call.get("name", "?") for call in message.tool_calls)
        extra = f" tools=[{names}]"
    elif isinstance(message, ToolMessage):
        extra = " tool_call_id='{message.tool_call_id}'"
    elif isinstance(message, SystemMessage):
        extra = " (system)"
    elif isinstance(message, HumanMessage):
        extra = " (human)"
    
    return f"{role}{extra}: {preview}"
