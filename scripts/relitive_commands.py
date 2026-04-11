import subprocess
import json


def start_process(command):
    use_shell = isinstance(command, str)
    subprocess.Popen(
        command,
        shell=use_shell,
        stdout=subprocess.DEVNULL,  # Redirect output to prevent pipe breaking
        stderr=subprocess.DEVNULL,
        stdin=subprocess.DEVNULL,
        start_new_session=True,      # This is the "disown" magic
        close_fds=True
    )

raw = subprocess.check_output(["hyprctl", "-j", "activeworkspace"], text=True)
workspace_id = str(json.loads(raw)["id"]) 

map_path = "/home/neros/.alice/data/map.json"

with open(map_path, "r") as f:
   map_commands = json.load(f)["map"]

try:
   start_process(map_commands[workspace_id])
except KeyError:
   start_process(map_commands["default"])
