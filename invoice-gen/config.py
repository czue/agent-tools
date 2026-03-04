import json
import tomllib
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv
import os


BASE_DIR = Path(__file__).parent


@dataclass
class ClientConfig:
    name: str
    country: str
    rate: float
    currency: str
    toggl_project_name: str
    line_item_description: str


@dataclass
class SenderConfig:
    name: str
    company: str
    address: str  # newline-separated lines
    tax_id: str
    email: str
    payment_details_usd: str
    payment_details_zar: str


def load_client(client_name: str) -> ClientConfig:
    """Load client config from clients/{client_name}.toml."""
    path = BASE_DIR / "clients" / f"{client_name}.toml"
    if not path.exists():
        raise FileNotFoundError(f"Client config not found: {path}")
    with open(path, "rb") as f:
        data = tomllib.load(f)
    return ClientConfig(**data)


def _env(key: str) -> str:
    """Get env var, converting literal \\n to real newlines."""
    return os.environ[key].replace("\\n", "\n")


def load_sender() -> SenderConfig:
    """Load sender config from environment variables."""
    load_dotenv(BASE_DIR / ".env")
    return SenderConfig(
        name=_env("SENDER_NAME"),
        company=_env("SENDER_COMPANY"),
        address=_env("SENDER_ADDRESS"),
        tax_id=_env("SENDER_TAX_ID"),
        email=_env("SENDER_EMAIL"),
        payment_details_usd=_env("PAYMENT_DETAILS_USD"),
        payment_details_zar=_env("PAYMENT_DETAILS_ZAR"),
    )


def _load_counter() -> dict:
    counter_path = BASE_DIR / "counter.json"
    with open(counter_path) as f:
        return json.load(f)


def _save_counter(data: dict) -> None:
    counter_path = BASE_DIR / "counter.json"
    with open(counter_path, "w") as f:
        json.dump(data, f, indent=2)


def get_next_invoice_number() -> int:
    """Read counter.json, increment, save, and return the new number."""
    data = _load_counter()
    next_num = data["last_invoice_number"] + 1
    data["last_invoice_number"] = next_num
    _save_counter(data)
    return next_num


def get_last_end_date(client_name: str) -> str | None:
    """Get the last invoice end date for a client, or None if no history."""
    data = _load_counter()
    return data.get("last_end_dates", {}).get(client_name)


def save_last_end_date(client_name: str, end_date: str) -> None:
    """Save the last invoice end date for a client."""
    data = _load_counter()
    if "last_end_dates" not in data:
        data["last_end_dates"] = {}
    data["last_end_dates"][client_name] = end_date
    _save_counter(data)
