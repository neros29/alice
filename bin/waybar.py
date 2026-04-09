#!/usr/bin/env python3
import subprocess
import json
import time
import sys

def get_cursor_y():
    """Return current cursor Y coordinate from hyprctl."""
    try:
        output = subprocess.check_output(["hyprctl", "-j", "cursorpos"], text=True)
        data = json.loads(output)
        return data.get("y")
    except (subprocess.CalledProcessError, json.JSONDecodeError, KeyError):
        return None

def toggle_waybar():
    """Run the toggle command."""
    subprocess.run(["omarchy-toggle-waybar"], check=False)

def main():
    # Initial state: Waybar is visible
    while subprocess.getoutput("pgrep waybar") == "":
        time.sleep(0.5)
    print("Waybar is running.")
    visible = True
    print("Script started. Monitoring cursor Y...", file=sys.stderr)

    try:
        while True:
            y = get_cursor_y()
            if y is None:
                # Skip if we couldn't get position
                time.sleep(0.1)
                continue

            # Logic
            if not visible and 0 <= y <= 5:
                toggle_waybar()
                visible = True
                print(f"Y={y} → Waybar turned ON", file=sys.stderr)
            elif visible and (y < 0 or y > 30):
                toggle_waybar()
                visible = False
                print(f"Y={y} → Waybar turned OFF", file=sys.stderr)

            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Script stopped by user.", file=sys.stderr)
        sys.exit(0)

if __name__ == "__main__":
    main()
