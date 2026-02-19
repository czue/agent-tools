"""
Push-to-talk speech-to-text toggle.

First invocation: starts recording from the microphone.
Second invocation: stops recording, transcribes, and types the result.
"""

import logging
import os
import signal
import subprocess
import time
from pathlib import Path

STATE_DIR = Path("/tmp/stt-toggle")
PID_FILE = STATE_DIR / "recorder.pid"
AUDIO_FILE = STATE_DIR / "recording.wav"
LOG_FILE = STATE_DIR / "stt.log"


def setup_logging():
    STATE_DIR.mkdir(exist_ok=True)
    logging.basicConfig(
        filename=str(LOG_FILE),
        level=logging.DEBUG,
        format="%(asctime)s %(levelname)s %(message)s",
    )


def notify(title: str, body: str = "", timeout_ms: int = 1500):
    """Show a desktop notification (non-blocking, best-effort)."""
    try:
        cmd = ["notify-send", "-t", str(timeout_ms), title]
        if body:
            cmd.append(body)
        subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        pass


def do_start():
    from .recorder import start_recording

    STATE_DIR.mkdir(exist_ok=True)
    AUDIO_FILE.unlink(missing_ok=True)

    proc = start_recording(str(AUDIO_FILE))
    PID_FILE.write_text(str(proc.pid))

    logging.info("Recording started (PID %d)", proc.pid)
    notify("Recording...", "Press hotkey again to stop")


def do_stop():
    from .config import load_config
    from .transcribers import get_transcriber
    from .typer import type_text

    pid = int(PID_FILE.read_text().strip())

    # SIGINT lets recorders finalize the WAV file cleanly
    logging.info("Stopping recording (PID %d)", pid)
    os.kill(pid, signal.SIGINT)
    time.sleep(0.5)

    PID_FILE.unlink(missing_ok=True)

    if not AUDIO_FILE.exists() or AUDIO_FILE.stat().st_size < 1000:
        logging.warning("No audio captured (file missing or too small)")
        notify("STT", "No audio captured")
        AUDIO_FILE.unlink(missing_ok=True)
        return

    notify("Transcribing...")

    config = load_config()
    transcriber = get_transcriber(config)

    try:
        text = transcriber.transcribe(str(AUDIO_FILE))
        logging.info("Transcribed: %s", text[:200])
    except Exception as e:
        logging.error("Transcription failed: %s", e)
        notify("STT Error", str(e)[:100])
        AUDIO_FILE.unlink(missing_ok=True)
        return

    AUDIO_FILE.unlink(missing_ok=True)

    if text.strip():
        type_text(text.strip(), method=config.get("paste_method", "clipboard"))
        logging.info("Text inserted")
    else:
        notify("STT", "No speech detected")
        logging.info("Empty transcription")


def main():
    setup_logging()

    try:
        if PID_FILE.exists():
            pid = int(PID_FILE.read_text().strip())
            os.kill(pid, 0)  # check if process is alive
            do_stop()
        else:
            do_start()
    except (ProcessLookupError, ValueError):
        # Stale PID file — clean up and start fresh
        logging.warning("Stale PID file, cleaning up")
        PID_FILE.unlink(missing_ok=True)
        AUDIO_FILE.unlink(missing_ok=True)
        do_start()
    except Exception as e:
        logging.error("Unexpected error: %s", e, exc_info=True)
        notify("STT Error", str(e)[:100])
