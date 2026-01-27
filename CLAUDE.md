# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is a Python project containing AI-powered tools for generating release notes for SaaS Pegasus, a Django SaaS boilerplate. The main agent uses pydantic-ai to orchestrate LLM calls with tools for git diff analysis and release notes reference.

## Commands

Run the agent:
```bash
uv run agent.py
```

Run with custom prompt:
```bash
uv run agent.py "Generate release notes for changes between v1.0 and v1.1"
```

Run the diff tool standalone:
```bash
uv run make_diff.py --from <commit/branch> --to <commit/branch> --repo-dir <path>
```

## Configuration

Copy `.env.example` to `.env` and configure:
- `REPO_PATH` - Path to the repository to analyze
- `RELEASE_NOTES_PATH` - Path to existing release notes for style reference
- `ANTHROPIC_API_KEY` or `OPENAI_API_KEY` - API key for the LLM provider
- `PYDANTIC_AI_MODEL` - Model identifier (default: `anthropic:claude-opus-4-5`)
- `LOG_LEVEL` - Logging verbosity (DEBUG, INFO, WARNING, ERROR)

## Architecture

**agent.py** - Main release notes agent using pydantic-ai
- Defines `release_notes_agent` with two tools: `make_diff` and `get_release_notes`
- Uses `Deps` dataclass to inject repository and release notes paths
- Saves generated notes to timestamped files in the repo directory

**make_diff.py** - Git diff utility
- `make_diff_string()` - Returns markdown diff report as string (used by agent)
- `make_diff()` - Writes diff report to file (CLI usage)
- Auto-resolves git pointers with fallback logic (main → develop → tags → HEAD)
- Filters out lock files (uv.lock, package-lock.json) by default

**handlers.py** - Event stream handler for logging tool calls during agent execution
