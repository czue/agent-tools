import subprocess
import time


def type_text(text: str, method: str = "type"):
    """Insert text at the current cursor position."""
    if method == "type":
        # Simulate keystrokes — works everywhere including terminals
        subprocess.run(
            ["xdotool", "type", "--clearmodifiers", text],
            check=True,
        )
    elif method == "clipboard":
        # Copy to clipboard — always sets the clipboard as a side effect,
        # but you'll need to paste manually (ctrl+v or ctrl+shift+v)
        subprocess.run(
            ["xclip", "-selection", "clipboard"],
            input=text.encode(),
            check=True,
        )
    else:
        raise ValueError(f"Unknown paste method: {method}")
