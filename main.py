#! /usr/bin/env python

from pylisp import *

source =  '(* (+ 1 2) 6)'
exp = parse(source)
val = leval(leval(exp))
print val

<<<<<<< HEAD
repl()
=======
#   
>>>>>>> fb7fa82e469c6ec276f696aa652e9cc6b6c7678c
