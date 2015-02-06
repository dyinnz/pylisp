#! /usr/bin/env python

from pylisp import *


#source =  '(* (+ 1 2) 6)'
#source = '(fread "text")'
#source = '(import "numpy")'
#source = '(** 2 10)'
source = '(print 10)'
val = leval(parse(source))
print val

#repl()
