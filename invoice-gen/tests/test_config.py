import json
import tomllib
from pathlib import Path
from unittest.mock import patch


def test_load_example_client():
    """Verify we can parse the example TOML config."""
    client_path = Path(__file__).parent.parent / "clients" / "example.toml"
    with open(client_path, "rb") as f:
        data = tomllib.load(f)
    assert data["name"] == "Acme Corp"
    assert data["rate"] == 100.00
    assert data["toggl_project_name"] == "acme"


def test_get_next_invoice_number(tmp_path):
    counter_file = tmp_path / "counter.json"
    counter_file.write_text(json.dumps({"last_invoice_number": 24}))

    from config import get_next_invoice_number

    with patch("config.BASE_DIR", tmp_path):
        assert get_next_invoice_number() == 25
        assert get_next_invoice_number() == 26

    data = json.loads(counter_file.read_text())
    assert data["last_invoice_number"] == 26
