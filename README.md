Agent Tools
===========

Agent tools I'm using in my various workflows.

## Skills

- **release-notes**: Generate release notes by analyzing git commits and diffs
- **generate-invoice**: Generate PDF invoices from Toggl time tracking data
- **backup-files**: Backup files to Backblaze B2 using rclone
- **open-as-html**: Convert markdown/output to styled HTML and open in browser
- **split-video**: Split wide (3840x1080) side-by-side videos into separate screen and camera files
- **transcript**: Generate HTML transcripts of Claude Code sessions using claude-code-transcripts

## Sub-Projects

- **[invoice-gen](./invoice-gen/)**: Standalone CLI tool for generating PDF invoices from Toggl time data
- **[speech-to-text](./speech-to-text/)**: Push-to-talk speech-to-text CLI for Linux (X11/GNOME)

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
