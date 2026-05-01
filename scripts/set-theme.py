from subprocess import run
import os
import json



class Main: 
    def __init__(self, root_dir) -> None:
        self.root_dir = os.path.expanduser(root_dir)
        self.dark = os.path.isfile(os.path.join(self.root_dir, "theme/current/dark"))
        self.theme_path = os.path.join(self.root_dir, "theme/current/theme.json")
        self._genrate_theme()
        self.theme = self._get_theme()
        self.theme_mode = self.theme["mode"]
    
    def _get_theme(self):
        with open(self.theme_path, "r") as f:
            return json.load(f)

    def _genrate_theme(self):
        background = os.path.join(self.root_dir, "theme/current/background")
        mode = "dark" if self.dark else "light"
        cmd = ["matugen", "image", "-m", mode, background, "--json", "hex", "--source-color-index", "0"]
        with open(self.theme_path, "w") as f:
            run(cmd, stdout=f)

    def _get_color(self, color: str):
        return self.theme["colors"][color][self.theme_mode]["color"]

    def gnome_theme(self):
        cmd = ["bash", os.path.join(self.root_dir, "scripts/set-gnome-theme.sh")]
        run(cmd)    

    def walker_theme(self):
        conf = f"""
@define-color selected-text {self._get_color("primary")};
@define-color text {self._get_color("on_background")};
@define-color base {self._get_color("background")};
@define-color border {self._get_color("on_background")};
@define-color foreground {self._get_color("background")};
@define-color background {self._get_color("on_background")};
        """
        conf_path = os.path.join(self.root_dir, "theme/current/walker.css")
        with open(conf_path, "w") as f:
            f.write(conf)


    def kitty_theme(self):
        conf = f"""
background               {self._get_color("background")}
        """              
        conf_path = os.path.join(self.root_dir, "theme/current/kitty.conf")
        with open(conf_path, "w") as f:
            f.write(conf)
        run(["killall", "-SIGUSR1", "kitty"])

    
    def main(self):
        self.gnome_theme()
        self.walker_theme()
        self.kitty_theme()

    

if __name__ == "__main__":
    main = Main("~/.alice/")
    main.main()

