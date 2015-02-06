#! /usr/bin/env python
from pylisp import *

__table = {'x': 1}

def _import(module, name=None):
    if not name: name = module
    m = __import__(module)
    __table.update({name:m})
    print __table

def find_symbol(table, symbol):
    pos = symbol.rfind('.')
    return getattr(table[symbol[:pos]], symbol[pos+1:])

#_import('pylisp', 'lisp')
#print find_symbol(__table, 'lisp.repl')

def interpret(filename):
    source = ''
    for line in open(filename).readlines():
        source += line + ' '
        paren = check_paren(source)
        if paren <= 0:
            if paren == 0:
                try: leval(parse(source))
                except Exception, e: print e
            elif paren < 0:
                print 'Error: unmatched parentheis!'
            source = ''

if __name__ == '__main__':
    import sys
    interpret(sys.argv[1])
    
