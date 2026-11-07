from __future__ import Annotations
from pydantic import BaseModel, Field
from typing import Literal

class TurnSummary(BaseModel):
    """This tells what the coding agent did in this turn."""
    summary: str = Field(
        description="A summary of what the coding agent did in this turn"
    )
    files_worked_with: list[str] = Field(
        description="Relative path of files you read, created or edited",
        default_factory=list
    )
    status: Literal["ok", "needs_input", "failed"] = Field(
        description="ok if the request is granted, needs_input if you must ask the user, failed if the request failed"
    )