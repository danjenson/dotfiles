set tabstop=4
set softtabstop=4
set shiftwidth=4
set expandtab
autocmd BufRead *.py set makeprg=python\ -c\ \"import\ py_compile,sys;\ sys.stderr=sys.stdout;\ py_compile.compile(r'%')\"
autocmd BufRead *.py set efm=%C\ %.%#,%A\ \ File\ \"%f\"\\,\ line\ %l%.%#,%Z%[%^\ ]%\\@=%m
autocmd BufRead *.py nmap <C-m> :!python %<CR>
autocmd BufWritePre *.py :call <SID>StripTrailingWhitespaces()
