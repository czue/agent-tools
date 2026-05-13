import os
from pathlib import Path

from dotenv import load_dotenv

PROJECT_DIR = Path(__file__).parent.parent


def load_config() -> dict:
    load_dotenv(PROJECT_DIR / ".env")

    return {
        "backend": os.getenv("STT_BACKEND", "openai"),
        "openai_api_key": os.getenv("STT_OPENAI_API_KEY", "") or os.getenv("OPENAI_API_KEY", ""),
        "model": os.getenv("STT_MODEL", ""),
        "paste_method": os.getenv("STT_PASTE_METHOD", "clipboard"),
    }
