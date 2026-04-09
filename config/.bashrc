# If not running interactively, don't do anything (leave this at the top of this file)
[[ $- != *i* ]] && return

# All the default Omarchy aliases and functions
# (don't mess with these directly, just overwrite them here!)
source ~/.local/share/omarchy/default/bash/rc
# Add your own exports, aliases, and functions here.
#
# Make an alias for invoking commands you use constantly
# alias p='python'
source ~/.config/bash/fzf.sh

alias gemma='ollama run gemma3:12b-it-q4_K_M'
alias fooocus_anime='~/Repos/Fooocus/start_anime.sh'
alias ddrive='~/Documents/projects/kao_download/myenv/bin/python3 ~/Documents/projects/kao_download/main.py'
alias git-commit='~/Documents/projects/git-commit/.venv/bin/python3 ~/Documents/projects/git-commit/git-commit-llm'
alias activate='source "$(/home/neros/.alice/bin/activate)"'
alias music="/home/neros/.alice/bin/music.sh"
alias rsiwd="systemctl restart iwd.service"
alias vim="nvim"

export MAKEFLAGS="-j$(nproc)"

set -o vi

# export FZF_DEFAULT_OPTS="--bind='ctrl-y:accept'"
#
# opencode
export PATH=/home/neros/.opencode/bin:$PATH

. "$HOME/.local/share/../bin/env"
. "$HOME/.cargo/env"
