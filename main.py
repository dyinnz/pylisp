#! /usr/bin/env python

from pylisp import *

source =  '(* (+ 1 2) 6)'
exp = parse(source)
val = leval(leval(exp))
print val

repl()
