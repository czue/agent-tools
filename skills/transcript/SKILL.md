---
name: transcript
description: Generate an HTML transcript of a Claude Code or Claude web session using claude-code-transcripts. Use when the user says "generate a transcript," "save this session," "export this conversation," "make a transcript," or wants to convert a session to HTML.
allowed-tools: Bash(uvx --from*claude-code-transcripts*), AskUserQuestion
---

# Generate Transcript

Generate an HTML transcript of a Claude Code or Claude web session using `uvx --from /home/czue/src/lib/claude-code-transcripts claude-code-transcripts`.

All commands use the local fork:
```
uvx --from /home/czue/src/lib/claude-code-transcripts claude-code-transcripts <command>
```

## Arguments

- `$0`: (optional) output mode — one of `open`, `gist`, `all`, or `web`

## Workflow

1. **Determine the output mode**:
   - If `$0` is provided and is a recognized mode (`open`, `gist`, `all`, `web`), use it.
   - Otherwise, default to **open** mode (Claude Code session opened in browser).

2. **Ask for the output detail level** (for single-session modes only):

   Use `AskUserQuestion` to ask which output mode the user wants:
   - **Full (Recommended)** — all content including tool calls, tool results, and thinking
   - **Compact** — hides tool results but shows tool calls and thinking
   - **Conversation** — text only, hides tool calls, tool results, and thinking

   This maps to the `--output-mode` flag: `full`, `compact`, or `conversation`.

3. **For single-session modes (`open` and `gist`), select the session**:

   a. **List recent sessions** using the `list` subcommand:
      ```bash
      uvx --from /home/czue/src/lib/claude-code-transcripts claude-code-transcripts list --json-output --limit 10
      ```
      This returns JSON with `path`, `summary`, `date`, `size`, and `project` for each session.

   b. **Present the sessions to the user** using `AskUserQuestion` with options built from the JSON.
      Format each option label like: `"2026-03-04 15:12 — can you make yourself a skill to generate transcripts..."`
      Use the `path` field to identify the selected session.

4. **Run the appropriate command** based on the mode:

   - **Open in browser** (`open`):
     ```bash
     uvx --from /home/czue/src/lib/claude-code-transcripts claude-code-transcripts json --open --output-mode <mode> "<selected_path>"
     ```

   - **Gist** (`gist`, the default):
     ```bash
     uvx --from /home/czue/src/lib/claude-code-transcripts claude-code-transcripts json --gist --output-mode <mode> "<selected_path>"
     ```

   - **All**:
     ```bash
     uvx --from /home/czue/src/lib/claude-code-transcripts claude-code-transcripts all --open
     ```
     Converts all local sessions to a browsable archive and opens it.

   - **Web**:
     ```bash
     uvx --from /home/czue/src/lib/claude-code-transcripts claude-code-transcripts web --open
     ```
     Note: this requires an interactive picker and may not work in Claude Code's terminal.
     Warn the user and try it anyway.

5. **Report results**: Tell the user what was generated and where the output went. If using gist mode, share the Gist URL from the command output.

## Notes

- The `json` subcommand is used instead of `local` to bypass the interactive picker (no TTY in Claude Code).
- For gist mode, the user needs `gh` (GitHub CLI) authenticated.
- The `--open` flag auto-opens results in the browser.
