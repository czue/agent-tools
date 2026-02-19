import shutil
import subprocess


def find_recorder() -> str:
    if shutil.which("rec"):
        return "sox"
    if shutil.which("ffmpeg"):
        return "ffmpeg"
    if shutil.which("arecord"):
        return "arecord"
    raise RuntimeError("No audio recorder found. Install sox, ffmpeg, or alsa-utils.")


def start_recording(output_path: str) -> subprocess.Popen:
    """Start recording 16kHz mono WAV audio. Returns the process handle."""
    recorder = find_recorder()

    if recorder == "sox":
        return subprocess.Popen(
            ["rec", "-q", "-r", "16000", "-c", "1", output_path],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    elif recorder == "ffmpeg":
        return subprocess.Popen(
            [
                "ffmpeg", "-y", "-f", "pulse", "-i", "default",
                "-ar", "16000", "-ac", "1", output_path,
            ],
            stdin=subprocess.PIPE,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    else:  # arecord
        return subprocess.Popen(
            ["arecord", "-f", "S16_LE", "-r", "16000", "-c", "1", output_path],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
