#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "=== Speech-to-Text Setup ==="
echo ""

# System dependencies
echo "Installing system dependencies (may need sudo)..."
sudo apt-get install -y sox xdotool xclip libnotify-bin

# Python dependencies
echo ""
echo "Installing Python dependencies..."
cd "$SCRIPT_DIR"
uv sync

# .env file
if [ ! -f "$SCRIPT_DIR/.env" ]; then
    cp "$SCRIPT_DIR/.env.example" "$SCRIPT_DIR/.env"
    echo ""
    echo "Created .env from .env.example — edit it to set your API key."
fi

# Wrapper script
cat > "$SCRIPT_DIR/stt-toggle" << WRAPPER
#!/bin/bash
cd "$SCRIPT_DIR"
exec uv run python -m stt
WRAPPER
chmod +x "$SCRIPT_DIR/stt-toggle"

echo ""
echo "=== Setup complete! ==="
echo ""
echo "Wrapper script: $SCRIPT_DIR/stt-toggle"
echo ""
echo "To test it manually:"
echo "  $SCRIPT_DIR/stt-toggle    # start recording"
echo "  $SCRIPT_DIR/stt-toggle    # stop, transcribe, type"
echo ""
echo "To add a GNOME keyboard shortcut:"
echo "  Settings → Keyboard → Keyboard Shortcuts → Custom Shortcuts"
echo "  Name:    Speech to Text"
echo "  Command: $SCRIPT_DIR/stt-toggle"
echo "  Shortcut: your choice (e.g. Ctrl+Alt+Space)"
echo ""
echo "Or run this to set Super+D automatically:"
echo "  bash $SCRIPT_DIR/setup-shortcut.sh"
