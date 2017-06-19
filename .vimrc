set shell=/bin/bash
set number
set mouse=a
set tabstop=4
set shiftwidth=4
set expandtab
set splitright
set splitbelow

set colorcolumn=81
hi ColorColumn guibg=#2d2d2d ctermbg=246

syntax on
colorscheme jellybeans

let mapleader="\\"
let maplocalleader="-"

" Convenient split pane movement
noremap <C-Down> <C-W><C-J>
noremap <C-Up> <C-W><C-K>
noremap <C-Right> <C-W><C-L>
noremap <C-Left> <C-W><C-H>

" Pytest
nnoremap <silent><Leader>f <Esc>:Pytest file<CR>
nnoremap <silent><Leader>n <Esc>:Pytest function<CR>
nnoremap <silent><Leader>c <Esc>:Pytest class<CR>
nnoremap <silent><Leader>m <Esc>:Pytest method<CR>

" Trim trailing whitespace
function! TrimSpace()
    %s/\s\+$//e
endfunction

" Replace crowded commas with comma and space
function! CommaSpace()
    %s/,\( \)\@!/, /g
endfunction

" Combining write processing functions
function! WriteProcess()
    call CommaSpace()
    call TrimSpace()
endfunction

" Process Python files and buffers on write
autocmd FileType python autocmd FileWritePre * silent! :call WriteProcess()
autocmd FileType python autocmd BufWritePre  * silent! :call WriteProcess()
