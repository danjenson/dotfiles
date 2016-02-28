" VIM MASTER

syntax on                   " syntax highlighting
set nocompatible            " be iMproved, require this
set backspace=2             " vim 7.4 fix

" set shell to run in as zsh
set shell=/bin/zsh
set shellcmdflag=-c

" set the runtime path to include Vundle and initialize
set rtp+=~/.vim/bundle/Vundle.vim
filetype off
call vundle#begin()

" put plugins here, run :PluginInstall to install
Plugin 'gmarik/Vundle.vim' " let Vundle manage Vundle, required
Plugin 'scrooloose/syntastic' "syntax checker
Plugin 'tpope/vim-surround'
Plugin 'tpope/vim-unimpaired'
Plugin 'tpope/vim-commentary'
Plugin 'delimitMate.vim'
Plugin 'Yggdroot/indentLine'
" Plugin 'vim-glsl'
" Plugin 'gerw/vim-latex-suite'

" NOTE: to install YouCompleteMe
" cd ~/.vim/bundle
" git clone git@github.com:Valloric/YouCompleteMe.git
" cd YouCompleteMe
" git submodule update --init --recursive
" dnf/apt-get/brew install cmake gcc-c++ python-libs python-devel
" ./install.sh
" add Plugin 'Valloric/YouCompleteMe' to your .vimrc_local

call vundle#end()           " required
filetype plugin indent on   " required

" Setters
set encoding=utf-8
set incsearch "Set search previewing
set hlsearch "Highlight search items
set cursorline "Add cursorline to view
set number "Set line numbering
set tabstop=4 "Set all the tabbing; autocmds in scripts override
set softtabstop=4 "Make sure this is equal to tabstop
set shiftwidth=4 "Used for > and < opeators
set expandtab "Changes tabs to spaces
set nocompatible "Gets out of old vim mode
set noerrorbells "No bells in terminal
set undolevels=1000 "Number of undos stored
set viminfo='50,"50 " '=marks for x files, "=registers for x files
set nofen "All folds are open
set foldmethod=indent "Indent based folding
set showcmd "Show command status
set showmatch "Flashes matching paren when one is typed
set showmode "Show editing mode in status (-- INSERT --)
set ruler "Show cursor position
set autoindent "Autoindents after returen
set tags=./tags;/ "Looks for tags in the pwd of the current file; stops at root
set path+=** "Searches directories recursively
set colorcolumn=81 "To help from going over 80 char limit
set textwidth=80 "Automatically wrap at 80 chars
set statusline+=%F "Full file path in statusline
set complete-=i "Don't search included files [slow]

" File-specific indentation
autocmd Filetype html setlocal ts=2 sts=2 sw=2

" make split windows easier to navigate
map <C-j> <C-w>j
map <C-k> <C-w>k
map <C-h> <C-w>h
map <C-l> <C-w>l
map <C-m> <C-w>_
nmap \| <C-w>v
nmap <C-_> <C-w>s

" ctags shortcuts
" open tag in new tab
map <C-\> :tab split<CR>:exec("tag ".expand("<cword>"))<CR>
" open tag in vertical split window
map <A-]> :vsp <CR>:exec("tag ".expand("<cword>"))<CR>

" colorscheme
colorscheme desert

" Source .vimrc_local if exists
if filereadable(glob("~/.vimrc_local"))
    source ~/.vimrc_local
endif

" YouCompleteMe
let g:ycm_autoclose_preview_window_after_completion = 1
let g:ycm_min_num_identifier_candidate_chars = 4
let g:ycm_enable_diagnostic_signs = 0
let g:ycm_error_symbol = 'x'
let g:ycm_warning_symbol = '!'
let g:ycm_server_keep_logfiles = 1
let g:ycm_server_log_level = 'debug'

" syntastic
let g:syntastic_cpp_compiler_options = ' -std=c++11'
nnoremap <leader>pg :YcmCompleter GoToDefinitionElseDeclaration<CR>
nnoremap <leader>pd :YcmCompleter GoToDefinition<CR>
nnoremap <leader>pc :YcmCompleter GoToDeclaration<CR>
