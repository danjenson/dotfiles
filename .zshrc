# Source local
if [ -f $HOME/.zshrc_local ]; then
    source $HOME/.zshrc_local
fi

# Set up the prompt
autoload -Uz promptinit
promptinit
prompt adam1

setopt histignorealldups sharehistory

# Keep 1000 lines of history within the shell and save it to ~/.zsh_history:
HISTSIZE=1000
SAVEHIST=1000
HISTFILE=~/.zsh_history

# Use modern completion system
autoload -Uz compinit
compinit

zstyle ':completion:*' auto-description 'specify: %d'
zstyle ':completion:*' completer _expand _complete _correct _approximate
zstyle ':completion:*' format 'Completing %d'
zstyle ':completion:*' group-name ''
zstyle ':completion:*' menu select=2
eval "$(dircolors -b)"
zstyle ':completion:*:default' list-colors ${(s.:.)LS_COLORS}
zstyle ':completion:*' list-colors ''
zstyle ':completion:*' list-prompt %SAt %p: Hit TAB for more, or the character to insert%s
zstyle ':completion:*' matcher-list '' 'm:{a-z}={A-Z}' 'm:{a-zA-Z}={A-Za-z}' 'r:|[._-]=* r:|=* l:|=*'
zstyle ':completion:*' menu select=long
zstyle ':completion:*' select-prompt %SScrolling active: current selection at %p%s
zstyle ':completion:*' use-compctl false
zstyle ':completion:*' verbose true

zstyle ':completion:*:*:kill:*:processes' list-colors '=(#b) #([0-9]#)*=0=01;31'
zstyle ':completion:*:kill:*' command 'ps -u $USER -o pid,%cpu,tty,cputime,cmd'

# CLI editing
export EDITOR=vim
export VISUAL=vim
setopt ignoreeof
setopt noclobber
setopt correct
bindkey -v
bindkey '^?' backward-delete-char
bindkey '^h' backward-delete-char
bindkey '^r' history-incremental-search-backward

# Safety
alias rm='rm -i'
alias mv='mv -i'
alias cp='cp -i'

# Functions
trpath () { echo $1 | tr ':' '\n'; }
path () { trpath $PATH; }
ppath () { trpath $PYTHONPATH; }
cpath () { trpath $CDPATH; }
zrc () { vim ~/.zshrc; }
sz () { source ~/.zshrc && echo '.zshrc REFRESHED!'; }
tls () { tmux list-sessions; }
tn () { tmux new -s $1; }
ta () {
    SESSIONS=($(tmux list-sessions | cut -d: -f1))
    if [ "${#SESSIONS[@]}" -eq 0 ]; then
        echo 'No tmux sessions currently running.'
    elif [ "${#SESSIONS[@]}" -eq 1 ]; then
        tmux attach -t ${SESSIONS[1]}
    else
        COUNT=0
        for SESSION in ${SESSIONS[@]} cancel
        do
            ((COUNT++))
            echo "$COUNT) $SESSION"
        done
        SELECTION=0
        echo -n -e '\nSELECTION: '
        read SELECTION
        while [ $SELECTION -lt 1 -o $SELECTION -gt $COUNT ]
        do
            echo '\nInvalid selection!'
            echo -n -e '\nSELECTION: '
            read SELECTION
        done
        if [ $SELECTION -eq $COUNT ]; then return; fi
        tmux attach -t ${SESSIONS[$((SELECTION))]}
        # arrays are zero indexed
    fi
}

# Aliases
alias ..='cd ..'
alias cl='clear'
alias ll='ls -lh'
alias m='less'
alias v='vim'
alias -s c,h,sh,html,css,js,php,py,sql=vim
