#!/bin/bash

# Change gnome modes
FILE_PATH="$HOME/.config/omarchy/current/theme.json"

# Check if the file exists and if the 'mode' key inside it is 'dark'
if [[ -f "$FILE_PATH" ]] && [[ $(jq -r '.mode' "$FILE_PATH") == "light" ]]; then
    # Condition is TRUE (File exists AND mode is dark)
    gsettings set org.gnome.desktop.interface color-scheme "prefer-light"
    gsettings set org.gnome.desktop.interface gtk-theme "Adwaita"
else
    gsettings set org.gnome.desktop.interface color-scheme "prefer-dark"
    gsettings set org.gnome.desktop.interface gtk-theme "Adwaita-dark"
fi

# Change gnome icon theme color
GNOME_ICONS_THEME=~/.alice/theme/current/icons.theme
if [[ -f $GNOME_ICONS_THEME ]]; then
    gsettings set org.gnome.desktop.interface icon-theme "$(<$GNOME_ICONS_THEME)"
else
    gsettings set org.gnome.desktop.interface icon-theme "Yaru-blue"
fi
