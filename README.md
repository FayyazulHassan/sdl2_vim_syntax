# SDL2 Vim syntax file

This file adds Vim/Neovim syntax highlighting for SDL2.

## Usage

Copy `sdl2.vim` to `~/.vim/syntax/` and add this to your `~/.vimrc`:

```viml
augroup sdl2
    autocmd!
    autocmd FileType c,cpp source ~/.vim/syntax/sdl2.vim
augroup END
```

## Generating the Syntax File

The file can be re-generated with `generator/sdl2_vim.py`. Run it like:

```sh
$ ./sdl2_vim.py /usr/include/SDL2/
```

The generator script requires [pycparser](https://github.com/eliben/pycparser). The `generator/utils` directory also belongs to `pycparser`.

## License

* `generator/sdl2_vim.py` public domain (unlicense)
* `generator/utils` copyright Eli Bendersky - <https://github.com/eliben/pycparser/blob/master/LICENSE>
