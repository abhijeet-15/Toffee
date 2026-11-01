from dataclasses import dataclass

@dataclass(frozen=True)
class Provider:
    name: str
    env_var: str
    isFree: bool
    model: str
    base_url: str | None