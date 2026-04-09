# Global fzf behavior
export FZF_DEFAULT_OPTS=''
# --- Global fzf options ---
export FZF_DEFAULT_OPTS='
    --height=60%
    --reverse
    --border
    --info=inline
    --bind ctrl-n:down,ctrl-p:up
    --height=60% 
    --reverse 
    --border 
    --info=inline
'

# zoxide + fzf deterministic jump
zi() {
    local dir
    dir=$(zoxide query -ls | awk '{print $2}' | fzf) || return
    cd "$dir"
}

# zoxide dir → file → nvim
nv() {
    local dir file
    dir=$(zoxide query -ls | awk '{print $2}' | fzf) || return
    file=$(fd . "$dir" | fzf) || return
    nvim "$file"
}

