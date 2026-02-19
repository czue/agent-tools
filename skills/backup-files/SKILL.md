---
name: backup-files
description: Backup files to Backblaze B2 using rclone. Use when the user wants to back up files, sync files to the cloud, or mentions rclone/B2 backups.
allowed-tools: Bash(rclone*), Bash(ls*), Bash(du*), Glob, AskUserQuestion
---

# Backup Files

Backs up local files to Backblaze B2 using rclone.

## Arguments

- `$0`: (optional) local path to back up
- `$1`: (optional) destination subfolder within the bucket

## Default Bucket

The default destination bucket is `b2:czue-youtube-backups`.

## Important: --max-depth

By default, always use `--max-depth 1` to avoid recursing into subdirectories. rclone will crawl the entire directory tree otherwise, which can be very slow and pick up unrelated files. Only omit `--max-depth` if the user explicitly asks to include subdirectories.

## Workflow

1. **Resolve the source path**:
   - If `$0` is provided, use it.
   - Otherwise, use `AskUserQuestion` to ask what to back up, with these options:
     - `~/Videos/` - Video files
     - `~/Music/` - Music files
     - `~/Documents/` - Documents
   - Verify the source path exists before proceeding.

2. **Resolve the destination path**:
   - If `$1` is provided, use `b2:czue-youtube-backups/$1` as the destination.
   - Otherwise, use `AskUserQuestion` to ask for the destination subfolder within the bucket, suggesting a sensible default based on the source path (e.g. `~/Videos/` → `videos`, `~/Documents/` → `documents`).

3. **Determine depth**:
   - Default to `--max-depth 1` (no subdirectory traversal).
   - If the user explicitly requests recursive/subdirectory backup, omit `--max-depth`.

4. **Show what will be backed up**:
   - Run `du -sh <source>` to show the total size.
   - Run a dry run first so the user can see what will happen:
     ```bash
     rclone copy <source> b2:czue-youtube-backups/<dest> --max-depth 1 --dry-run
     ```
   - Show the user a summary and ask for confirmation before proceeding.

5. **Run the backup**:
   ```bash
   rclone copy <source> b2:czue-youtube-backups/<dest> --max-depth 1 --progress --stats=5s
   ```
   Run this in the foreground so the user can see progress.

6. **Report results**: Summarize what was backed up and the destination.
