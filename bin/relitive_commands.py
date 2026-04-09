import subprocess
import json

raw = subprocess.getoutput("hyprctl -j activeworkspace")
workspace_id = str(json.loads(raw)["id"]) 
map_path = "/home/neros/.alice/data/map.json"
with open(map_path, "r") as f:
   map_commands = json.load(f)["map"]
try:
   subprocess.getoutput(map_commands[workspace_id])
except KeyError:
   subprocess.getoutput(map_commands["defualt"])
