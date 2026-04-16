#!/usr/bin/env python3
import os
import socket
import subprocess
import logging
import time
from pathlib import Path

# --- CONFIGURATION ---
# Update these paths as needed
TARGET_LINK = Path.home() / ".config/omarchy/current/background"
# The command to run when a monitor is added
AWWW_COMMAND = [
    "awww", "img", str(TARGET_LINK),
    "--transition-type", "wipe",
    "--transition-duration", "2",
    "--transition-fps", "144",
    "--resize", "crop"
]

# Setup Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

def get_hyprland_socket():
    """Dynamically locates the Hyprland socket2 path."""
    signature = os.environ.get("HYPRLAND_INSTANCE_SIGNATURE")
    if not signature:
        return None

    runtime_dir = os.environ.get("XDG_RUNTIME_DIR")
    if not runtime_dir:
        return None

    socket_path = Path(runtime_dir) / "hypr" / signature / ".socket2.sock"
    return str(socket_path) if socket_path.exists() else None

def update_wallpaper():
    """Executes the awww command."""
    logging.info("Monitor change detected! Updating wallpapers...")
    time.sleep(3)
    try:
        # Using subprocess.run is safer and more reliable than os.system
        result = subprocess.run(AWWW_COMMAND, check=True, capture_output=True, text=True)
        logging.info("Wallpaper update successful.")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        logging.error(f"Wallpaper update failed! Error: {e.stderr.strip()}")
    except Exception as e:
        logging.error(f"Unexpected error during wallpaper update: {e}")

def monitor_loop():
    """Main loop that handles socket connection and reconnection."""
    logging.info("Wallpaper monitor service started.")

    while True:
        socket_path = get_hyprland_socket()

        if not socket_path:
            logging.warning("Hyprland socket not found. Retrying in 5s...")
            time.sleep(5)
            continue

        try:
            # Create a Unix Domain Socket connection
            with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as client:
                logging.info(f"Connecting to Hyprland socket: {socket_path}")
                client.connect(socket_path)

                # Use makefile to treat the socket like a file (allows line-by-line reading)
                with client.makefile('r', encoding='utf-8') as socket_file:
                    for line in socket_file:
                        line = line.strip()
                        if line.startswith("monitoradded"):
                            update_wallpaper()

        except (ConnectionRefusedError, FileNotFoundError):
            logging.error("Hybrland socket connection lost. Attempting to reconnect...")
            time.sleep(2)
        except Exception as e:
            logging.error(f"Socket error: {e}")
            time.sleep(2)

if __name__ == "__main__":
    try:
        monitor_loop()
    except KeyboardInterrupt:
        logging.info("Service stopped by user.")
    except Exception as e:
        logging.critical(f"Service crashed: {e}")
