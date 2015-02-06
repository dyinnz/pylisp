#! /usr/bin/env python

from pylisp import *


#source =  '(* (+ 1 2) 6)'
#source = '(fread "text")'
#source = '(import "numpy")'
#source = '(** 2 10)'
#source = '(print (+ 1 2))'
source = '(print "hello* world")'
print get_tokens(source)
val = leval(parse(source))
print val

#repl()
