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


def is_safe_workspace(path: Path) -> bool:
    try:
        work_dir = get_work_dir()
        work_dir.mkdir(parents=True, exist_ok=True)

        candidate = (work_dir / Path(path).relative_to(Path(path).anchor)).resolve()

        if candidate.is_relative_to(work_dir):
            return True
        
        raise ValueError(f"Path {path} escapes the working directory {work_dir}")
    
    except (ValueError, OSError):
        return False