" Plugins
syntax on
filetype indent plugin on
" Install this from github for easy plugins
if filereadable(glob("~/.vim/autoload/pathogen.vim"))
    execute pathogen#infect() 
endif

" Toggle supertab with \<tab> (<leader><tab>)
let SuperTabMappingForward = '<leader><space>'
let g:SuperTab_tab = 0
function! ToggleSuperTabMap()
  if g:SuperTab_tab == 1
      let g:SuperTabMappingForward = "<leader><space>"

      let g:SuperTabMappingTabLiteral = "<tab>"
      so ~/.vim/plugin/supertab.vim
      let g:SuperTab_tab = 0
      echo "SuperTab key = <leader><space>"
  else
      let g:SuperTabMappingForward = "<tab>"
      let g:SuperTabMappingTabLiteral = "<leader><space>"
      so ~/.vim/plugin/supertab.vim
      let g:SuperTab_tab = 1
      echo "SuperTab key = <tab>"
  endif
endfunction
map <leader><tab> :call ToggleSuperTabMap()<CR>
imap <leader><tab> <esc>:call ToggleSuperTabMap()<CR>a

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
set tags=./tags;/ "Looks for tags in the pwd of the current file; stops at root
set path+=** "Searches directories recursively
set colorcolumn=81 "To help from going over 80 char limit

" File-specific indentation
autocmd BufRead, BufNewFile *.py, *.c, *.h set ts=2 sts=2 sw=2
autocmd BufRead, BufNewFile *.ruby set ts=2 sts=2 sw=2

" Command that listen for events
autocmd BufWritePre *.py,*.js :call <SID>StripTrailingWhitespaces()

" make split windows easier to navigate
map <C-j> <C-w>j
map <C-k> <C-w>k
map <C-h> <C-w>h
map <C-l> <C-w>l
map <C-m> <C-w>_
nmap \| <C-w>v
nmap <C-_> <C-w>s

" Custom functions
" Make pdf using latex
command! Ltx call Ltx()
function Ltx()
    execute ':w | !pdflatex %'
endfunction

" Shorten syntastic check
command! Chk call Chk()
function Chk()
    execute ':SyntasticCheck'
endfunction

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

" Source .vimrc_local if exists
if filereadable(glob("~/.vimrc_local"))
    source ~/.vimrc_local
endif
