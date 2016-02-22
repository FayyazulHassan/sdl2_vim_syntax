SDL2 vim syntax file
====================

Usage
-----
Copy `sdl2.vim` to `~/.vim/syntax` and add this line to `~/.vimrc`

    au FileType c,cpp source ~/.vim/syntax/sdl2.vim

Generating syntax file
----------------------
File can be re-generated with `generator/sdl2_vim.py`. This script requires
[pycparser]. `generator/utils` also belongs to `pycparser`, which some dummy
additions.


[pycparser]: https://github.com/eliben/pycparser
