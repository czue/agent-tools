import math
import httpx
import os

from dotenv import load_dotenv
from pathlib import Path

load_dotenv(Path(__file__).parent / ".env")


def get_toggl_auth() -> tuple[str, str]:
    """Return (username, password) for Toggl HTTP Basic auth."""
    return (os.environ["TOGGL_API_TOKEN"], "api_token")


def get_workspace_id() -> str:
    return os.environ["TOGGL_WORKSPACE_ID"]


def get_project_id(workspace_id: str, project_name: str) -> int:
    """Look up Toggl project ID by name."""
    auth = get_toggl_auth()
    resp = httpx.get(
        f"https://api.track.toggl.com/api/v9/workspaces/{workspace_id}/projects",
        auth=auth,
    )
    resp.raise_for_status()
    projects = resp.json()
    for p in projects:
        if p["name"].lower() == project_name.lower():
            return p["id"]
    raise ValueError(f"Project '{project_name}' not found in Toggl. Available: {[p['name'] for p in projects]}")


def get_total_hours(workspace_id: str, project_id: int, start_date: str, end_date: str) -> float:
    """
    Fetch total tracked hours from Toggl Reports API v3 summary endpoint.

    Returns total hours rounded to nearest quarter hour (0.25).
    """
    auth = get_toggl_auth()
    resp = httpx.post(
        f"https://api.track.toggl.com/reports/api/v3/workspace/{workspace_id}/summary/time_entries",
        json={
            "start_date": start_date,
            "end_date": end_date,
            "project_ids": [project_id],
        },
        auth=auth,
    )
    resp.raise_for_status()
    data = resp.json()

    # Response is {"groups": [{"sub_groups": [{"seconds": N}, ...], ...}, ...]}
    total_seconds = 0
    for group in data.get("groups", []):
        for sub in group.get("sub_groups", []):
            total_seconds += sub.get("seconds", 0)

    total_hours = total_seconds / 3600
    return round_to_quarter(total_hours)


def round_to_quarter(hours: float) -> float:
    """Round to nearest quarter hour."""
    return round(hours * 4) / 4
