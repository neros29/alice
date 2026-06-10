from subprocess import SubprocessError, run
from pathlib import Path
import os
import json


class Main: 
    def __init__(self, root_dir) -> None:
        self.root_dir = Path(root_dir)
        self.theme_dir = self.root_dir / "theme" / "current"
        self.mode = "light" if (self.theme_dir / "light").exists() else "dark"
        self.theme = self._genrate_theme()
    

    def _genrate_theme(self):
        background = self.theme_dir / "background"
        cmd = ["matugen", "image", "-m", self.mode, background, "--json", "hex", "--source-color-index", "0"]
        try:
            result = run(cmd, capture_output=True, text=True, check=True)
            (self.theme_dir / "theme.json").write_text(result.stdout)
            return json.loads(result.stdout)
        except Exception as e:
            print(f"Error {e} Exiting program")
            exit(1)

    def _get_color(self, color: str):
        return self.theme["colors"][color][self.mode]["color"]

    def gnome_theme(self):
        cmd = ["bash", self.root_dir / "scripts" / "set-gnome-theme.sh"]

    def hyprland_theme(self):
        active_border = self._get_color("primary")
        inactive_border = self._get_color("secondary_container")
        conf = f"""
hl.config({{ general = {{ col = {{ active_border = "{active_border}", inactive_border = "{inactive_border}" }} }} }})
        """              
        conf_path = self.theme_dir / "hyprland.lua"
        conf_path.write_text(conf)

    def walker_theme(self):
        conf = f"""
@define-color selected-text {self._get_color("primary")};
@define-color text {self._get_color("on_background")};
@define-color base {self._get_color("background")};
@define-color border {self._get_color("on_background")};
@define-color foreground {self._get_color("background")};
@define-color background {self._get_color("on_background")};
        """
        conf_path = self.theme_dir / "walker.css"
        conf_path.write_text(conf)

    def music_launcher_theme(self):
        conf = f"""
{{
    "background": "{self._get_color("background")}",
    "foreground": "{self._get_color("on_background")}",
    "surface_bg": "{self._get_color("secondary_container")}"
}}
        """              
        conf_path = self.theme_dir / "music-launcher.json"
        conf_path.write_text(conf)
        run(["killall", "-SIGUSR1", "kitty"])


    def kitty_theme(self):
        conf = f"""
background {self._get_color("background")}
foreground {self._get_color("on_background")}

selection_background {self._get_color("primary")}
selection_foreground {self._get_color("background")}

cursor {self._get_color("secondary")}
cursor_text_color {self._get_color("background")}

active_tab_foreground    {self._get_color("secondary_container")}
active_tab_background   {self._get_color("primary")} 

inactive_tab_foreground  {self._get_color("primary")}
inactive_tab_background {self._get_color("secondary_container")} 
        """              
        conf_path = self.theme_dir / "kitty.conf"
        conf_path.write_text(conf)
        run(["killall", "-SIGUSR1", "kitty"])

    
    def main(self):
        self.hyprland_theme()
        self.gnome_theme()
        self.walker_theme()
        self.kitty_theme()
        self.music_launcher_theme()

if __name__ == "__main__":
    path = Path("~/.alice/").expanduser()
    main = Main(path)
    main.main()

