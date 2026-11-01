from fnmatch import fnmatch
from pathlib import Path

from src.config.config import get_work_dir

BLOCKED_PATHS_PATTERNS = [
    ".env",
    ".git",
    ".pem",
    ".key",
    ".secret",
    ".git/**",
    "*.log",
    "*.p12"
]

def normalized_path(path: str) -> str:
    normalized = Path(path).as_posix()

    normalized = normalized.removeprefix("./")
    
    return normalized


def is_blocked_path(path: str) -> str:
    normalized = normalized_path(path)
    return any(fnmatch(normalized, pattern) for pattern in BLOCKED_PATHS_PATTERNS)


def resolve_work_path(path: str) -> Path:
    """
    Resolves a requested path against the workspace root.
    Returns the absolute Path object if safe, raises ValueError if it escapes.
    """
    work_dir = get_work_dir().resolve()
    work_dir.mkdir(parents=True, exist_ok=True)
    
    raw_path = Path(path)
    
    if raw_path.anchor:
        raw_path = raw_path.relative_to(raw_path.anchor)
        
    candidate = (work_dir / raw_path).resolve()
    
    if candidate.is_relative_to(work_dir):
        return candidate
        
    raise ValueError(f"Path '{path}' escapes the working directory '{work_dir}'")


