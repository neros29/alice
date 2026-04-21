from subprocess import run
import os
import json



class Main: 
    def __init__(self, root_dir) -> None:
        self.root_dir = os.path.expanduser(root_dir)
        self.theme = self._get_theme()
        self.theme_mode = self.theme["mode"]
    
    def _get_theme(self):
        path = os.path.join(self.root_dir, "theme/current/theme.json")
        with open(path, "r") as f:
            return json.load(f)

    def gnome_theme(self):
        cmd = ["bash", os.path.join(self.root_dir, "scripts/set-gnome-theme.sh")]
        run(cmd)    

    def kitty_theme(self):
        conf = f"""
background               {self.theme["colors"]["background"][self.theme_mode]["color"]}
        """              
        conf_path = os.path.join(self.root_dir, "theme/current/kitty.conf")
        with open(conf_path, "w") as f:
            f.write(conf)
        run(["killall", "-SIGUSR1", "kitty"])

    
    def main(self):
        self.gnome_theme()
        self.kitty_theme()


if __name__ == "__main__":
    main = Main("~/.alice/")
    main.main()

