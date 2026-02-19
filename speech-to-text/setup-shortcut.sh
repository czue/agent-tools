#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SHORTCUT_KEY="${1:-<Super>d}"

BINDING_BASE="/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings"

# Find an available slot
SLOT=0
while dconf read "${BINDING_BASE}/custom${SLOT}/name" &>/dev/null; do
    EXISTING_NAME=$(dconf read "${BINDING_BASE}/custom${SLOT}/name" 2>/dev/null)
    if [[ "$EXISTING_NAME" == "'Speech to Text'" ]]; then
        echo "Updating existing shortcut in slot custom${SLOT}..."
        break
    fi
    SLOT=$((SLOT + 1))
done

SLOT_PATH="${BINDING_BASE}/custom${SLOT}/"

# Register the slot in the keybindings list
EXISTING=$(gsettings get org.gnome.settings-daemon.plugins.media-keys custom-keybindings)
if [[ "$EXISTING" == "@as []" ]]; then
    gsettings set org.gnome.settings-daemon.plugins.media-keys custom-keybindings "['${SLOT_PATH}']"
elif [[ "$EXISTING" != *"${SLOT_PATH}"* ]]; then
    NEW=$(echo "$EXISTING" | sed "s|]|, '${SLOT_PATH}']|")
    gsettings set org.gnome.settings-daemon.plugins.media-keys custom-keybindings "$NEW"
fi

# Set the shortcut properties
dconf write "${SLOT_PATH}name" "'Speech to Text'"
dconf write "${SLOT_PATH}command" "'${SCRIPT_DIR}/stt-toggle'"
dconf write "${SLOT_PATH}binding" "'${SHORTCUT_KEY}'"

echo "Keyboard shortcut set: ${SHORTCUT_KEY} → Speech to Text"
echo "Change it in Settings → Keyboard → Custom Shortcuts"
