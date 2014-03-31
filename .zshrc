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
setopt noclobber
setopt correct
bindkey -v
bindkey '^?' backward-delete-char
bindkey '^h' backward-delete-char
bindkey '^r' history-incremental-search-backward

# Add current directory to PATH
export PATH=$PATH:.  # NEVER DO THIS AS ROOT

# Safety
alias rm='rm -i'
alias mv='mv -i'
alias cp='cp -i'

# aliases
alias ..='cd ..'
alias cl='clear'
alias ll='ls -lh'
alias m='less'
alias v='vim'
alias sz='source ~/.zshrc && echo .zshrc REFRESHED!'
alias ta='tmux attach'
alias tls='tmux list'
alias zrc='vim ~/.zshrc'
alias -s c,h,sh,html,css,js,php,py,sql=vim
