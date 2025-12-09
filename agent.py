"""Release notes generator agent for SaaS Pegasus."""

from __future__ import annotations

import asyncio
import os
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Final

from handlers import agent_event_stream_handler
from dotenv import load_dotenv  # type: ignore[import-not-found]
from pydantic_ai import Agent, RunContext  # type: ignore[import-not-found]

from make_diff import make_diff_string

PROJECT_ROOT = Path(__file__).parent
load_dotenv(dotenv_path=PROJECT_ROOT / ".env", override=False)

REPO_ENV_VAR: Final = "PEGASUS_REPO_PATH"
RELEASE_NOTES_ENV_VAR: Final = "PEGASUS_RELEASE_NOTES_PATH"
MODEL_ENV_VAR: Final = "PYDANTIC_AI_MODEL"


def _required_env(name: str) -> str:
    try:
        return os.environ[name]
    except KeyError as exc:
        raise RuntimeError(f"Missing required environment variable: {name}") from exc


DEFAULT_REPO_PATH = Path(_required_env(REPO_ENV_VAR))
DEFAULT_RELEASE_NOTES_PATH = Path(_required_env(RELEASE_NOTES_ENV_VAR))
DEFAULT_MODEL = os.environ.get(MODEL_ENV_VAR, "anthropic:claude-opus-4-5")


BASE_INSTRUCTIONS = """You are helping to generate the release notes for an upcoming version of SaaS Pegasus---a
Django SaaS boilerplate built on top of cookicutter.

You will be given a diff summary file containing a set of changes that have been made in
this release. Your job is to draft the release notes according in the same style used
in the current release notes (`src/content/docs/release-notes.md`).

Important instructions:

- Read the existing release notes to get a feel for the style.
- The general format is: 1-2 sentences describing the release followed by a detailed list of changes.
- If a feature is large you can call it out into its own section at the top, but if there
  aren't any large features there is no need to do this.
- Wherever possible use information from the commit messages to understand the intent of the changes.
- Do NOT EVER mention cookiecutter. If a change only affects cookiecutter markup then translate
  the practical implications of that change in human-readable terms. E.g. "Fixed a bug that only
  applied when teams were enabled".
- For library upgrades there is no need to mention specific libraries unless explicitly called
  out in a commit message."""
TOOL_GUIDANCE = f"""
You can call tools to gather context:
- Use `get_release_notes` to load the current published notes for style reference. Path: {DEFAULT_RELEASE_NOTES_PATH}.
- Use `make_diff` to pull the markdown-formatted git diff summary for the requested commit range. Default range is main -> develop when none is provided.

Workflow: read the reference notes to mirror tone and structure, call `make_diff` to gather the changes, then draft updated notes. Keep the summary concise (1-2 sentences) followed by a detailed bullet list. Translate template-only changes into user-facing impacts and never mention cookiecutter explicitly.
"""

AGENT_PROMPT = f"{BASE_INSTRUCTIONS}\n\n{TOOL_GUIDANCE}"


@dataclass
class Deps:
    repo_path: Path = DEFAULT_REPO_PATH
    release_notes_path: Path = DEFAULT_RELEASE_NOTES_PATH


release_notes_agent = Agent(
    DEFAULT_MODEL,
    instructions=AGENT_PROMPT,
    deps_type=Deps,
    retries=2,
)


@release_notes_agent.tool
async def make_diff(  # type: ignore[override]
    ctx: RunContext[Deps],
    from_ref: str | None = None,
    to_ref: str | None = None,
    ignore_patterns: list[str] | None = None,
) -> str:
    """Return a markdown diff report for the configured repository."""

    def _run():
        return make_diff_string(
            from_pointer=from_ref,
            to_pointer=to_ref,
            ignore_patterns=ignore_patterns,
            repo_dir=ctx.deps.repo_path,
        )

    return await asyncio.to_thread(_run)


@release_notes_agent.tool
async def get_release_notes(ctx: RunContext[Deps]) -> str:
    """Load the existing release notes for style reference."""
    path = ctx.deps.release_notes_path

    def _read():
        if path.exists():
            return path.read_text()
        else:
            raise FileNotFoundError(f"Release notes file not found at {path}")

    return await asyncio.to_thread(_read)


async def run_release_notes_agent(prompt: str | None = None) -> str:
    """Run the agent with the provided user prompt."""
    deps = Deps()
    user_prompt = prompt or "Draft release notes for the latest changes in the repo."
    result = await release_notes_agent.run(user_prompt, deps=deps, event_stream_handler=agent_event_stream_handler)
    saved_path = save_release_notes(result.output, deps.repo_path)
    return result.output, saved_path


def save_release_notes(content: str, dest_dir: Path) -> Path:
    """Persist generated release notes to disk."""
    dest_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    path = dest_dir / f"release-notes-{timestamp}.md"
    path.write_text(content)
    return path


def main():
    prompt = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else None
    output, saved_path = asyncio.run(run_release_notes_agent(prompt))
    print("Response:\n")
    print(output)
    print(f"\nSaved draft to: {saved_path}")


if __name__ == "__main__":
    main()
