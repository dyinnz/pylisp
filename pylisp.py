#! /usr/bin/env python
'''
Date: 2015/02/06-07
Description: Hust.UniqueStudio.Hackday
'''

__table = {}
__specail_forms = {}

from calc import calc

# parse

def get_value(token):
    token = atom(token)
    if isinstance(token, int) or isinstance(token, float):
        return token
    elif len(token) > 2 and token[0]=='\"' and token[-1]=='\"':
        return token[1:-1]
    else: 
        return __table[token]

def atom(token):
    try: return int(token)
    except ValueError:
        try: return float(token)
        except ValueError:
            return token # the same as str(token)

def get_tokens(source):
    tokens = []
    pos = 0
    is_str = False
    token = ''
    while pos < len(source):
        c = source[pos]
        if c in ['(', ')', '{', '}']:
            if len(token) != 0: tokens.append(token)
            token = ''
            tokens.append(c)
        elif c == ' ' and not is_str:
            if len(token) != 0: tokens.append(token)
            token = ''
        elif c == '\"':
            is_str = not is_str
            token += c
        else:
            token += c
        pos += 1
    return tokens

def parse(source):
    stack = [[]]
    try: 
        tokens = get_tokens(source)
        pos = 0
        while pos < len(tokens):
            token = tokens[pos]
            if '(' == token: stack.append([])
            elif ')' == token: 
                exp = stack.pop()
                if len(exp) > 0: stack[-1].append(exp)
                else: raise SyntaxError('Empty list!')
            elif '{' == token:
                d = {}
                pos += 1
                while tokens[pos] != '}':
                    d[get_value(tokens[pos])] = get_value(tokens[pos+1])
                    pos += 2
                stack[-1].append(d)
            else: 
                stack[-1].append(atom(token))
            pos += 1
        return stack.pop()[0]
    except Exception, e:
        print 'Error:', e

# built-in function

def _import(module, name=None):
    if not name: name = module
    __table.update({name: __import__(module)})

def _print(*l):
    for x in l: print x,
    print ''

def _read(prompt=''):
    return raw_input(prompt)

def _get(d, k, default=None):
    if default: return d.get(k, default)
    else: return d[k]

def _assoc(d, k, v):
    nd = d.copy(); nd[k] = v
    return nd

def _disassoc(d, k):
    nd = d.copy(); nd.pop(k)
    return nd

def _call(obj, fun, *args):
    return getattr(obj, fun, *args)

def build_table():
    import math, operator as op
    __table.update(vars(math))
    __table.update({
        '+': op.add, '-': op.sub, '*': op.mul, '/': op.div, '**': pow,
        '<': op.lt, '>': op.gt, '<=': op.le, '>=': op.ge, '=': op.eq})

    __table.update({
        'int': int, 'str': str, 'float': float,
        'nth': lambda x, n: x[n],
        'get': _get, 'assoc': _assoc, 'disassoc': _disassoc,
        'pair': lambda x, y: (x, y),
        '.': _call})

    __table.update({
        'fwrite': lambda f, s: open(f, 'w').write(s),
        'fread': lambda f: open(f).read(),
        'list': lambda *x: list(x),
        'set': lambda *x: set(x),
        'dict': lambda x,y: dict(zip(x,y)), 
        'zero?': lambda x: x == 0, 
        'read': _read, 'print': _print, 'import': _import, 
        'map': map,
        'reduce': reduce,
        'max': max,
        'min': min,
        'abs': abs,
        'len': len, 
        'append':  op.add,  
        'apply':   apply,
        'begin':   lambda *x: x[-1],
        'first':     lambda x: x[0],
        'second': lambda x: x[1],
        'rest':     lambda x: x[1:], 
        'last': lambda x: x[-1],
        'cons':    lambda x,y: [x] + y,
        'eq?':     op.is_, 
        'equal?':  op.eq, 
        'len':  len, 
        'list?':   lambda x: isinstance(x,list), 
        'max':     max,
        'min':     min,
        'not':     op.not_,
        'null?':   lambda x: x == [], 
        'number?': lambda x: isinstance(x, int) and isinstance(x, float),   
        'procedure?': callable,
        'round':   round,
        'symbol?': lambda x: isinstance(x, str),
        'reverse': lambda x: x[::-1],
        '//': lambda a, b: a // b,
        'remainder':calc.rem,
        '%':   lambda a, b: a % b,
        'gcd':      calc.gcd,
        'lcm':      calc.lcm,
        'expt':     lambda x, y: x ** y,
        'number?':  lambda x: isinstance(x, int) or isinstance(x, float),  
        'complex?': lambda x: isinstance(x, complex),
        'boolean?': lambda x: isinstance(x, bool),
        'rational?':lambda x: isinstance(x, float),
        'integer?': lambda x: isinstance(x, int),
        'zero?':    lambda x: x == 0,
        'positive?':lambda x: x > 0,
        'negative?':lambda x: x < 0,
        'odd?':     lambda x: x % 2 == 1,
        'even?':    lambda x: x % 2 == 0,

        })

build_table()

# eval

def find_symbol(table, symbol):
    pos = symbol.rfind('.')
    return getattr(table[symbol[:pos]], symbol[pos+1:])

def leval(exp, local={}):
    if isinstance(exp, str):
        if len(exp) > 2 and exp[0]=='\"' and exp[-1]=='\"': return exp[1:-1]
        elif exp in local: return local[exp]
        elif exp in __table: return __table[exp]
        elif '.' in exp: return find_symbol(__table, exp)
        #else: raise NameError('No such name "%s"!'% (exp,))
        return exp
    elif not isinstance(exp, list):
        return exp
    first = exp[0]
    if first == 'quote' or first == '\'':
        return exp[1:]
    elif first == 'if':
        (_, test, t, f) = exp
        return leval(t, local) if leval(test, local) else leval(f, local)
    elif first == 'def':
        #(_, var, sub) = exp[0],exp[1],exp[2:]
        if(len(exp)==3):
            (_, var, sub) = exp
            __table[var] = leval(sub, local)
        elif(len(exp)==4):
            (_, var, fnvar, sub) = exp
            __table[var] = Lamfn(fnvar, sub, local)
    elif first == 'do':
        l = local.copy()
        updates = {}
        (_, v, t) = exp
        for var in v:
            (var, val, update) = var
            l[var] = val
            updates[var] = update
        (test, res) = t
        while not leval(test,l):
            for k in updates:
                l[k] = leval(updates[k], l)
        return leval(res, l)
    elif first == 'fn':
        (_, var, sub) = exp
        return Lamfn(var, sub, local)
    elif first == 'let':
        (_, var, sub) = exp[0], exp[1], exp[2:]
        l = local.copy()
        for v,a in var:
            l[v] = a;
        for s in sub:
            leval(s, l)
    elif first == 'loop':
        (_, init, cond) = exp
        local[init[0]] = leval(init[1])
        (_, test, out, recur) = cond
        if recur[0] != 'recur':
            raise 'Syntax Error'
        while not leval(test):
            local[recur[1]] = leval(recur[2])
        return leval(out, local)
    elif first == 'eval':
        [leval(sub, local) for sub in exp[1:-1]]
        return leval(exp[-1])
    else: 
        fn = leval(first, local)
        args = [leval(sub, local) for sub in exp[1:]]
        return fn(*args)

# repl

def check_paren(source_in):
    paren = 0
    for c in source_in:
        if c == '(': paren += 1
        elif c == ')': paren -= 1
    return paren

def repl(prompt='pylisp'):
    prompt += '=>'
    pro = prompt
    source = ''
    while True: 
        source += raw_input(pro) + ' '
        paren = check_paren(source)
        if paren <= 0:
            if paren == 0:
                try : print leval(parse(source))
                except Exception, e: print e
            elif paren < 0:
                print 'Error: unmacthed parentheis!'
            pro = prompt
            source = ''
        else:
            pro = '.'*len(prompt[:-2]) + '=>' + ' '*paren*2

class Lamfn:
    def __init__(self, var, sub, local):
        self.var, self.sub, self.local = var, sub, local
    def __call__(self, *args):
        local = self.local.copy()
        local.update(dict(zip(self.var, args)))
        return leval(self.sub, local)

def cut_comment(line):
    pos = line.find(';')
    return line if pos==-1 else line[:pos]

def interpret(filename):
    source = ''
    for line in open(filename).readlines():
        source += cut_comment(line) + ' '
        source = source.strip()
        if len(source) == 0: continue
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
    if len(sys.argv) >= 2:
        argstr = sys.argv[1]
        if argstr == '-repl': repl() 
        else :interpret(sys.argv[1])

