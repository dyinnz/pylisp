from pylisp import *

#s = __import__('pylisp')

__table = {'x': 1}

def _import(module, name=None):
    if not name: name = module
    m = __import__(module)
    __table.update({name:m})
    print __table

def find_symbol(table, symbol):
    pos = symbol.rfind('.')
    return getattr(table[symbol[:pos]], symbol[pos+1:])

_import('pylisp', 'lisp')
print find_symbol(__table, 'lisp.repl')

