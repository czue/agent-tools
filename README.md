Agent Tools
===========

Agent tools I'm using in my various workflows.

## Skills

- **release-notes**: Generate release notes by analyzing git commits and diffs

## Installation (Claude Code)

```bash
# Add the marketplace
/plugin marketplace add czue/agent-tools

# Install all skills from the marketplace
/plugin install agent-tools
```

### Usage

```
/release-notes v2024.12.1 HEAD /path/to/reference-notes.mdx
```

Or just ask Claude things like "What changed since the last release?"

## Installation (Python Agent)

The release notes generator can also be run as a standalone Python agent using pydantic-ai.

First set up your environment variables:

```bash
cp .env.example .env
```

Add your API key(s), select a model, and configure paths.

Then run the agent:

```bash
uv run agent.py
```
