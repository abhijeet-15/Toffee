import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
PROMPTS_DIR = PROJECT_ROOT / "prompts"
DEFAULT_WORK_DIR = PROJECT_ROOT / "workspace"
AGENT_NAME = "Toffee"
MAX_MODEL_CALLS_PER_RUN = int(os.getenv("MAX_MODEL_CALLS_PER_RUN", "10"))
MAX_READ_BYTES = int(os.getenv("MAX_READ_BYTES", "1000000"))

def hitl_enabled() -> bool:
    return bool(os.getenv("HITL_ENABLED", "True"))

def get_work_dir() -> Path:
    override = os.getenv("WORK_DIR", "").strip()
    
    if override:
        return Path(override).expanduser().resolve()

    return DEFAULT_WORK_DIR.resolve()

print(hitl_enabled())
print(get_work_dir())
