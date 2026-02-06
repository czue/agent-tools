---
name: release-notes
description: Generate release notes by analyzing git commits and diffs. Use when asked to create release notes, changelog entries, or summarize code changes between versions.
allowed-tools: Bash(python:*), Read, Write, AskUserQuestion
---

# Release Notes Generator for SaaS Pegasus

Generate professional release notes for code changes between git refs. Can be run from any directory.

## Arguments

- `$0`: from_ref (e.g., "v1.0", commit SHA, or branch name)
- `$1`: to_ref (e.g., "v1.1", "HEAD", or branch name)
- `$2`: (optional) path to the git repository to analyze
- `$3`: (optional) path to reference release notes file for style matching
- `$4`: (optional) output file path (default: prompt user)

## Defaults

Users can customize these defaults. If a default is set and the corresponding argument is not provided, use the default without prompting.

- `default_repo_path`: (none)
- `default_release_notes_path`: (none)

## Workflow

1. **Resolve the repo path**:
   - If `$2` is provided, use it.
   - Else if `default_repo_path` is set, use that.
   - Otherwise, use `AskUserQuestion` to ask the user: "What is the path to the git repository to analyze?" with an option for the current directory (`.`) and an option to enter a custom path.

2. **Resolve the release notes reference file**:
   - If `$3` is provided, use it.
   - Else if `default_release_notes_path` is set, use that.
   - Otherwise, use `AskUserQuestion` to ask: "Is there an existing release notes file to use as a style reference?" with options "No reference file" and "Enter a path".

3. **Read reference notes** (if a reference path was resolved) to match tone and structure.

4. **Run the diff script** to get commit and file change data:
   ```bash
   python <skill-dir>/scripts/make_diff.py --from "$0" --to "$1" --repo-dir <resolved_repo_path>
   ```

5. **Draft release notes** following the guidelines below.

6. **Output handling**: If `$4` is provided, write to that file. Otherwise, display the notes and ask if user wants to save them.

## Style Guidelines

- Format: 1-2 sentences describing the release, followed by a detailed list of changes
- Large features can have their own section at the top; otherwise, use a flat list
- Use commit messages to understand intent of changes
- Highlight substantial changes from diffs that aren't in commit messages
- **Never mention cookiecutter** - translate cookiecutter markup changes to human terms
- **Ignore commits starting with "invisible:" or "tool:"** - don't mention them or their files
- For library upgrades, only mention specific libraries if explicitly called out in commits

## Additional Resources

- For formatting examples and style reference, see [examples.md](examples.md)
