#! /usr/bin/env python

from pylisp import *


#source =  '(* (+ 1 2) 6)'
#source = '(fread "text")'
source = '(import "dypart")'
val = leval(parse(source))
source = '(dypart.test)'
val = leval(parse(source))
print val

#repl()
