---
name: release-notes
description: Generate release notes by analyzing git commits and diffs. Use when asked to create release notes, changelog entries, or summarize code changes between versions.
allowed-tools: Bash(python:*), Read, Write
---

# Release Notes Generator for SaaS Pegasus

Generate professional release notes for code changes between git refs.

## Arguments

- `$0`: from_ref (e.g., "v1.0", commit SHA, or branch name)
- `$1`: to_ref (e.g., "v1.1", "HEAD", or branch name)
- `$2`: (optional) path to reference release notes file for style matching
- `$3`: (optional) output file path (default: prompt user)

## Workflow

1. **Read reference notes** (if `$2` provided) to match tone and structure
2. **Run the diff script** to get commit and file change data:
   ```bash
   python <skill-dir>/scripts/make_diff.py --from "$0" --to "$1" --repo-dir .
   ```
3. **Draft release notes** following the guidelines below
4. **Output handling**: If `$3` is provided, write to that file. Otherwise, display the notes and ask if user wants to save them.

## Style Guidelines

- Format: 1-2 sentences describing the release, followed by a detailed list of changes
- Large features can have their own section at the top; otherwise, use a flat list
- Use commit messages to understand intent of changes
- Highlight substantial changes from diffs that aren't in commit messages
- **Never mention cookiecutter** - translate cookiecutter markup changes to human terms
- **Ignore commits starting with "invisible:" or "tool:"** - don't mention them or their files
- For library upgrades, only mention specific libraries if explicitly called out in commits
