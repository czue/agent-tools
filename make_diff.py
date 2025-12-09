#!/usr/bin/env python
"""
Generate a markdown file with git diff information between two commits/branches.
"""

import subprocess
import sys
from datetime import datetime
from pathlib import Path


def run_git_command(cmd, check=True, shell=False, cwd=None):
    """Run a git command and return the output."""
    try:
        if isinstance(cmd, str) and shell:
            # If shell=True, use shell execution
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                check=check,
                cwd=cwd,
            )
        else:
            # If cmd is a list or shell=False, use list execution (safer)
            if isinstance(cmd, str):
                # Split string into list for shell=False
                import shlex
                cmd = shlex.split(cmd)
            result = subprocess.run(
                cmd,
                shell=False,
                capture_output=True,
                text=True,
                check=check,
                cwd=cwd,
            )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        cmd_str = cmd if isinstance(cmd, str) else ' '.join(cmd)
        print(f"Error running git command: {cmd_str}", file=sys.stderr)
        print(f"Error: {e.stderr}", file=sys.stderr)
        raise


def resolve_commit_pointer(pointer, repo_dir=None):
    """Resolve a git pointer (branch, tag, or commit) to a commit SHA."""
    if not pointer:
        return None
    sha = run_git_command(
        ["git", "rev-parse", pointer], check=True, shell=False, cwd=repo_dir
    )
    return sha


def get_commit_info(sha, repo_dir=None):
    """Get commit information for a given SHA."""
    commit_msg = run_git_command(
        ["git", "log", "-1", "--pretty=format:%s", sha],
        check=True,
        shell=False,
        cwd=repo_dir,
    )
    commit_date = run_git_command(
        ["git", "log", "-1", "--pretty=format:%ai", sha],
        check=True,
        shell=False,
        cwd=repo_dir,
    )
    return {
        "sha": sha,
        "message": commit_msg,
        "date": commit_date,
    }


def get_commit_list(from_sha, to_sha, repo_dir=None):
    """Get list of commits between two SHAs."""
    if from_sha == to_sha:
        return []
    commits = run_git_command(
        ["git", "log", "--pretty=format:%H|%s|%ai", f"{from_sha}..{to_sha}"], check=True, shell=False, cwd=repo_dir
    )
    if not commits:
        return []
    commit_list = []
    for line in commits.split('\n'):
        parts = line.split('|', 2)
        if len(parts) == 3:
            commit_list.append({
                "sha": parts[0],
                "message": parts[1],
                "date": parts[2],
            })
    return commit_list


def get_changed_files(from_sha, to_sha, ignore_patterns=None, repo_dir=None):
    """Get list of changed files with their status."""
    if from_sha == to_sha:
        return []
    if ignore_patterns is None:
        ignore_patterns = []

    files = run_git_command(
        ["git", "diff", "--name-status", f"{from_sha}..{to_sha}"],
        check=True,
        shell=False,
        cwd=repo_dir,
    )
    if not files:
        return []
    file_list = []
    for line in files.split('\n'):
        if line:
            status = line[0]
            filepath = line[1:].strip()
            # Check if file should be ignored
            if not any(pattern in filepath for pattern in ignore_patterns):
                file_list.append({
                    "status": status,
                    "path": filepath,
                })
    return file_list


def get_full_diff(from_sha, to_sha, ignore_patterns=None, repo_dir=None):
    """Get the full diff output, filtering out ignored files."""
    if from_sha == to_sha:
        return ""
    if ignore_patterns is None:
        ignore_patterns = []

    # Get the full diff
    diff = run_git_command(
        ["git", "diff", f"{from_sha}..{to_sha}"], check=True, shell=False, cwd=repo_dir
    )

    if not diff or not ignore_patterns:
        return diff

    # Filter out diffs for ignored files
    # Git diff format: "diff --git a/path b/path" starts a new file block
    lines = diff.split('\n')
    filtered_lines = []
    skip_block = False

    for line in lines:
        # Check if this line starts a new file diff block
        if line.startswith('diff --git'):
            # Extract the file path from "diff --git a/path b/path"
            # Try to get path from "b/path" first, fallback to "a/path"
            if ' b/' in line:
                file_path = line.split(' b/')[-1]
            elif ' a/' in line:
                file_path = line.split(' a/')[-1]
            else:
                file_path = line

            # Check if this file should be ignored
            skip_block = any(pattern in file_path for pattern in ignore_patterns)
            if not skip_block:
                filtered_lines.append(line)
        elif skip_block:
            # Skip lines until we hit the next diff block
            continue
        else:
            # Regular diff line, include it
            filtered_lines.append(line)

    return '\n'.join(filtered_lines)


def _resolve_range(from_pointer, to_pointer, repo_dir=None, verbose=False):
    """Resolve pointers, applying defaults that mirror the CLI behavior."""
    resolved_from = from_pointer
    resolved_to = to_pointer

    if not resolved_from:
        try:
            run_git_command(
                ["git", "rev-parse", "--verify", "main"],
                check=True,
                shell=False,
                cwd=repo_dir,
            )
            resolved_from = "main"
        except Exception:
            try:
                run_git_command(
                    ["git", "rev-parse", "--verify", "develop"],
                    check=True,
                    shell=False,
                    cwd=repo_dir,
                )
                resolved_from = "develop"
            except Exception:
                try:
                    resolved_from = run_git_command(
                        ["git", "describe", "--tags", "--abbrev=0", "HEAD^"],
                        check=False,
                        shell=False,
                        cwd=repo_dir,
                    )
                    if not resolved_from:
                        resolved_from = "main"
                except Exception:
                    resolved_from = "main"

    if not resolved_to:
        try:
            run_git_command(
                ["git", "rev-parse", "--verify", "develop"],
                check=True,
                shell=False,
                cwd=repo_dir,
            )
            resolved_to = "develop"
        except Exception:
            try:
                run_git_command(
                    ["git", "rev-parse", "--verify", "main"],
                    check=True,
                    shell=False,
                    cwd=repo_dir,
                )
                resolved_to = "main"
            except Exception:
                resolved_to = "HEAD"

    if verbose:
        print(f"Resolving 'from' pointer: {resolved_from}")
    from_sha = resolve_commit_pointer(resolved_from, repo_dir=repo_dir)
    if verbose:
        print(f"  -> {from_sha}")

    if verbose:
        print(f"Resolving 'to' pointer: {resolved_to}")
    to_sha = resolve_commit_pointer(resolved_to, repo_dir=repo_dir)
    if verbose:
        print(f"  -> {to_sha}")

    if from_sha == to_sha and verbose:
        print("Warning: 'from' and 'to' point to the same commit. Generating diff anyway.")

    return resolved_from, resolved_to, from_sha, to_sha


def build_markdown(
    from_pointer,
    to_pointer,
    from_sha,
    to_sha,
    ignore_patterns=None,
    repo_dir=None,
):
    """Render markdown describing the diff."""
    from_info = get_commit_info(from_sha, repo_dir=repo_dir)
    to_info = get_commit_info(to_sha, repo_dir=repo_dir)
    commits = get_commit_list(from_sha, to_sha, repo_dir=repo_dir)
    changed_files = get_changed_files(from_sha, to_sha, ignore_patterns, repo_dir=repo_dir)
    full_diff = get_full_diff(from_sha, to_sha, ignore_patterns, repo_dir=repo_dir)

    lines = [
        "# Git Diff Report",
        "",
        "## Commit Range",
        f"- **From**: `{from_sha[:7]}` ({from_pointer or from_sha})",
        f"  - Message: {from_info['message']}",
        f"  - Date: {from_info['date']}",
        f"- **To**: `{to_sha[:7]}` ({to_pointer or to_sha})",
        f"  - Message: {to_info['message']}",
        f"  - Date: {to_info['date']}",
        "",
    ]

    if commits:
        lines.extend(
            [
                "## Commits",
                "",
            ]
        )
        for commit in commits:
            lines.append(f"- `{commit['sha'][:7]}` - {commit['message']} ({commit['date']})")
        lines.append("")
    else:
        lines.extend(
            [
                "## Commits",
                "",
                "*No commits between the specified range.*",
                "",
            ]
        )

    if changed_files:
        lines.extend(
            [
                "## Changed Files",
                "",
            ]
        )
        status_map = {
            "A": "Added",
            "M": "Modified",
            "D": "Deleted",
            "R": "Renamed",
            "C": "Copied",
        }
        for file_info in changed_files:
            status_desc = status_map.get(file_info["status"], file_info["status"])
            lines.append(f"- **{status_desc}**: `{file_info['path']}`")
        lines.append("")
    else:
        lines.extend(
            [
                "## Changed Files",
                "",
                "*No files changed.*",
                "",
            ]
        )

    lines.extend(
        [
            "## Full Diff",
            "",
            "```diff",
            full_diff,
            "```",
        ]
    )

    return "\n".join(lines)


def generate_markdown(from_pointer, to_pointer, from_sha, to_sha, output_path, ignore_patterns=None, repo_dir=None):
    """Generate the markdown file with all diff information."""
    markdown = build_markdown(
        from_pointer,
        to_pointer,
        from_sha,
        to_sha,
        ignore_patterns=ignore_patterns,
        repo_dir=repo_dir,
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w') as f:
        f.write(markdown)

    return output_path


def make_diff_string(from_pointer=None, to_pointer=None, ignore_patterns=None, repo_dir=None):
    """Return the diff report as a markdown string instead of writing to disk."""
    ignore_patterns = ignore_patterns or ['uv.lock', 'package-lock.json']
    from_pointer, to_pointer, from_sha, to_sha = _resolve_range(
        from_pointer, to_pointer, repo_dir=repo_dir, verbose=False
    )
    return build_markdown(
        from_pointer,
        to_pointer,
        from_sha,
        to_sha,
        ignore_patterns=ignore_patterns,
        repo_dir=repo_dir,
    )


def make_diff(from_pointer=None, to_pointer=None, output_dir=None, ignore_patterns=None, repo_dir=None):
    """
    Generate a markdown file with git diff information.

    Args:
        from_pointer: Git pointer (branch, tag, or commit) for the start of the range.
                     Defaults to previous tag or 'develop' if not provided.
        to_pointer: Git pointer for the end of the range. Defaults to 'HEAD' if not provided.
        output_dir: Directory to save the output file. Defaults to 'output/' in project root.
        ignore_patterns: List of file patterns to ignore (e.g., ['uv.lock', 'package-lock.json']).
                        Defaults to ['uv.lock', 'package-lock.json'].

    Returns:
        Path to the generated markdown file.
    """
    ignore_patterns = ignore_patterns or ['uv.lock', 'package-lock.json']
    from_pointer, to_pointer, from_sha, to_sha = _resolve_range(
        from_pointer, to_pointer, repo_dir=repo_dir, verbose=True
    )

    # Determine output directory
    if not output_dir:
        base_dir = Path(repo_dir) if repo_dir else Path(__file__).parent.parent
        output_dir = base_dir / "output"
    else:
        output_dir = Path(output_dir)

    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    from_short = from_sha[:7]
    to_short = to_sha[:7]
    filename = f"diff_{timestamp}_{from_short}_to_{to_short}.md"
    output_path = output_dir / filename

    print(f"\nGenerating diff report...")
    if ignore_patterns:
        print(f"Ignoring files matching: {', '.join(ignore_patterns)}")
    generate_markdown(
        from_pointer,
        to_pointer,
        from_sha,
        to_sha,
        output_path,
        ignore_patterns,
        repo_dir=repo_dir,
    )
    print(f"Diff report saved to: {output_path}")

    return output_path


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate a git diff report in markdown format.")
    parser.add_argument("--from", dest="from_pointer", help="Git pointer for the start of the range")
    parser.add_argument("--to", dest="to_pointer", help="Git pointer for the end of the range")
    parser.add_argument("--output-dir", help="Directory to save the output file")
    parser.add_argument("--repo-dir", dest="repo_dir", help="Path to the git repository to diff")
    args = parser.parse_args()

    make_diff(
        from_pointer=args.from_pointer,
        to_pointer=args.to_pointer,
        output_dir=args.output_dir,
        repo_dir=args.repo_dir,
    )
