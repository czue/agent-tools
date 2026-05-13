# Speech-to-Text

Push-to-talk speech-to-text for Linux (X11/GNOME). Press a hotkey to start recording,
press it again to stop — transcribed text appears wherever your cursor is.

## How it works

1. **First hotkey press** — starts recording from your microphone
2. **Second hotkey press** — stops recording, sends audio to a transcription backend, copies the result to your clipboard (paste with Ctrl+V / Ctrl+Shift+V)
3. Desktop notifications show recording/transcribing status

## Requirements

- Ubuntu (tested on 24.04) with X11
- Python 3.10+
- [uv](https://docs.astral.sh/uv/)
- An OpenAI API key (for the default backend)

## Setup

1. **Run the install script:**

   ```bash
   bash install.sh
   ```

   This installs system dependencies (`sox`, `xdotool`, `xclip`, `libnotify-bin`),
   Python dependencies, and creates the `stt-toggle` wrapper script.

2. **Configure your API key:**

   Edit `.env` (created automatically from `.env.example`) and set your OpenAI API key:

   ```
   STT_OPENAI_API_KEY=sk-your-key-here
   ```

   Or if `OPENAI_API_KEY` is already in your environment, it will use that automatically.

3. **Set up a keyboard shortcut:**

   **Option A — GNOME Settings (manual):**
   Settings → Keyboard → Keyboard Shortcuts → Custom Shortcuts
   - Name: `Speech to Text`
   - Command: `/full/path/to/speech-to-text/stt-toggle`
   - Shortcut: your choice (e.g. `Ctrl+Alt+Space`)

   **Option B — Automatic:**

   ```bash
   bash setup-shortcut.sh              # defaults to Super+D
   bash setup-shortcut.sh '<Ctrl><Alt>space'  # or pick your own
   ```

## Configuration

All config is in `.env`:

| Variable | Default | Description |
|---|---|---|
| `STT_BACKEND` | `openai` | Transcription backend: `openai` or `faster-whisper` |
| `STT_OPENAI_API_KEY` | | OpenAI API key (falls back to `OPENAI_API_KEY` env var) |
| `STT_MODEL` | *(backend default)* | Model name (see below) |
| `STT_PASTE_METHOD` | `clipboard` | `clipboard` (copies only, paste manually) or `type` (xdotool keystrokes) |

### Transcription backends

**OpenAI API** (default) — best accuracy, requires internet, ~$0.003–0.006/min:
- `whisper-1` (default) — solid all-around
- `gpt-4o-mini-transcribe` — cheapest
- `gpt-4o-transcribe` — best accuracy

**faster-whisper** — fully local/offline, no API key needed:

```bash
uv sync --extra local
```

Then set `STT_BACKEND=faster-whisper` in `.env`. Models:
- `base.en` (default) — fast on CPU, good accuracy
- `small.en` — slower, better accuracy
- `large-v3-turbo` — best accuracy, needs a GPU to be practical

## Troubleshooting

- **Logs:** `/tmp/stt-toggle/stt.log`
- **Text not appearing:** The default `clipboard` method only copies the transcript — paste it yourself with Ctrl+V (or Ctrl+Shift+V in terminals). Set `STT_PASTE_METHOD=type` if you want xdotool to type it directly at the cursor instead (note: can be flaky in some terminals).
- **No audio captured:** Check that your mic is working (`arecord -d 2 test.wav && aplay test.wav`). The recorder uses `sox`/`rec` if available, otherwise falls back to `ffmpeg`.
- **Stale state:** If the toggle gets stuck, delete `/tmp/stt-toggle/recorder.pid`.
