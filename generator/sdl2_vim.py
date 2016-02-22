#!/usr/bin/python

import sys;
import os;
import re;
from pycparser import c_parser, c_ast, parse_file, preprocess_file;

class visitor(c_ast.NodeVisitor):
	__slots__ = ['functions', 'types', 'enums', 'defines'];

	def __init__(self):
		self.functions = [];
		self.types = [];
		self.enums = [];
		self.defines = [];

	def visit_FuncDecl(self, node):
		t = None;
		if isinstance(node.type, c_ast.TypeDecl):
			t = node.type;
		elif isinstance(node.type, c_ast.PtrDecl):
			t = node.type.type;

		if t != None:
			if t.declname[:4] == "SDL_":
				self.functions.append(t.declname);

	def visit_TypeDecl(self, node):
		if isinstance(node.type, c_ast.Enum):
			self.visit_Enum(node.type);

		if isinstance(node.declname, str) and len(node.declname) > 4 and (node.declname[:4] == "SDL_" or node.declname[:4] == "Sint" or node.declname[:4] == "Uint"):
			self.types.append(node.declname);

	def visit_Enumerator(self, node):
		if node.name[:3] == "SDL":
			self.enums.append(node.name);

	def visit_Enum(self, node):
		for v in node.values.enumerators:
			self.visit_Enumerator(v);

def generate_output(filename, v):
	with open(filename, "wt") as f:
		f.write('''" Vim syntax file
" Language: C SDL2 library extension
" Generated By: sdl2_vim.py

''');

		f.write("syn keyword sdl2_function %s\n" % (" ".join(v.functions)));
		f.write("syn keyword sdl2_type %s\n" % (" ".join(v.types)));
		f.write("syn keyword sdl2_enum %s\n" % (" ".join(v.enums)));
		f.write("syn keyword sdl2_define %s\n" % (" ".join(v.defines)));

		f.write('''
" Default highlighting
if version >= 508
  if version < 508
    command -nargs=+ HiLink hi link <args>
  else
    command -nargs=+ HiLink hi def link <args>
  endif
  HiLink sdl2_function Function
  HiLink sdl2_type Type
  HiLink sdl2_enum Constant
  HiLink sdl2_define Constant
  delcommand HiLink
endif
''');

def process_file(filename, incpath):
	cppargs = ["-Iutils/fake_libc_include", "-I%s" % incpath,
			"-DDECLSPEC=",
			"-D_SDL_platform_h=1",
			"-D_SDL_endian_h=1",
			"-DSDL_FORCE_INLINE=", "-D__attribute__(x)=",
	];
	ast = parse_file(filename, use_cpp=True, cpp_args=cppargs);
	v = visitor();
	v.visit(ast);

	del ast;

	cppargs.append("-dM");
	defines_text = preprocess_file(filename, cpp_args=cppargs);
	for s in defines_text.split("\n"):
		if s[:8] == "#define ":
			s = s[8:];
			m = re.search("(SDL_[A-Za-z0-9_]+)", s);
			if m != None:
				d = m.group(0);
				if isinstance(d, str) and len(d) > 4 and d == d.upper():
					v.defines.append(d);

	generate_output("sdl2.vim", v);

if len(sys.argv) > 1:
	process_file(os.path.join(sys.argv[1], "SDL.h"), sys.argv[1]);
else:
	print("use: %s path/to/SDL2/headers/directory" % sys.argv[0]);
