---
name: split-video
description: Split a wide (3840x1080) side-by-side video into separate screen and camera files using ffmpeg. Use when the user says "split this file" or wants to split a wide video recording.
allowed-tools: Bash(ffmpeg*), Bash(ffprobe*), Glob, AskUserQuestion
---

# Split Wide Video

Splits a 3840x1080 side-by-side video into two 1920x1080 files: one for the screen capture (left half) and one for the camera (right half).

## Arguments

- `$0`: (optional) path to the video file to split

## Workflow

1. **Resolve the input file**:
   - If `$0` is provided, use it.
   - Otherwise, search for video files (*.mp4, *.mkv, *.mov, *.avi) in these directories in order:
     1. The current working directory
     2. `~/` (home directory)
     3. `~/Videos/`
   - If exactly one video file is found across all searched directories, confirm with the user that it's the right one.
   - If multiple video files are found, use `AskUserQuestion` to ask which file to split.
   - If no video files are found in any of those locations, use `AskUserQuestion` to ask for the file path.

2. **Verify the video dimensions** using ffprobe:
   ```bash
   ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=p=0 "<input_file>"
   ```
   - Expected: 3840x1080 (or similar wide format where width is ~2x height).
   - If dimensions don't match, warn the user and ask if they want to proceed anyway.

3. **Split the video** into two files:
   - Screen capture (left half):
     ```bash
     ffmpeg -i "<input_file>" -filter:v "crop=1920:1080:0:0" -c:v libx264 -crf 18 -preset fast -c:a aac -b:a 192k "<base>-screen.mp4"
     ```
   - Camera (right half):
     ```bash
     ffmpeg -i "<input_file>" -filter:v "crop=1920:1080:1920:0" -c:v libx264 -crf 18 -preset fast -c:a aac -b:a 192k "<base>-cam.mp4"
     ```
   Where `<base>` is the input filename without its extension.

4. **Report results**: Tell the user the names of the two output files created.
