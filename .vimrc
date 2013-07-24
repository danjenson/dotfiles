" Source .vimfb if exists
if filereadable(glob("~/.vimfb"))
    source ~/.vimfb
endif

" Plugins
syntax on
filetype indent plugin on
"Install this from github for easy plugins
execute pathogen#infect() 

" Setters
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
set tags=tags;/

" make split windows easier to navigate
map <C-j> <C-w>j
map <C-k> <C-w>k
map <C-h> <C-w>h
map <C-l> <C-w>l
map <C-m> <C-w>_

" Command that listen for events
autocmd BufWritePre *.py,*.js :call <SID>StripTrailingWhitespaces()

" Custom functions
" Set tabstop, softtabstop and shiftwidth to the same value
command! -nargs=* Stab call Stab()
function! Stab()
  let l:tabstop = 1 * input('set tabstop = softtabstop = shiftwidth = ')
  if l:tabstop > 0
    let &l:sts = l:tabstop
    let &l:ts = l:tabstop
    let &l:sw = l:tabstop
  endif
  call SummarizeTabs()
endfunction
  
function! SummarizeTabs()
  try
    echohl ModeMsg
    echon 'tabstop='.&l:ts
    echon ' shiftwidth='.&l:sw
    echon ' softtabstop='.&l:sts
    if &l:et
      echon ' expandtab'
    else
      echon ' noexpandtab'
    endif
  finally
    echohl None
  endtry
endfunction

" Strip trailing whitespace
function! <SID>StripTrailingWhitespaces()
    " Preparation: save last search, and cursor position.
    let _s=@/
    let l = line(".")
    let c = col(".")
    " Do the business:
    %s/\s\+$//e
    " Clean up: restore previous search history, and cursor position
    let @/=_s
    call cursor(l, c)
endfunction
