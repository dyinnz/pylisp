'''
Date: 2015/02/06-07
Description: Hust.UniqueStudio.Hackday
'''

__table = {}
__specail_forms = {}

# parse

def atom(token):
    try: return int(token)
    except ValueError:
        try: return float(token)
        except ValueError:
            return token # the same as str(token)

def parse(source):
    stack = [[]]
    try: 
        for token in source.replace('(',' ( ').replace(')',' ) ').split():
            if '(' == token: stack.append([])
            elif ')' == token: 
                exp = stack.pop()
                if len(exp) > 0: stack[-1].append(exp)
                else: raise SyntaxError('Empty list!')
            else: stack[-1].append(atom(token))
        return stack.pop()[0]
    except:
        raise SyntaxError('Syntax Error')

# built-in function

def _import(module, name=None):
    if not name: name = module
    __table.update({name: __import__(module)})

def _print(x):
    print x

def build_table():
    import math, operator as op
    __table.update(vars(math))
    __table.update({
        '+': op.add, '-': op.sub, '*': op.mul, '/': op.div, '**': pow})
    
    __table.update({
        'fwrite': lambda f, s: open(f, 'w').write(s),
        'fread': lambda f: open(f).read(),
        'print': _print, 'import': _import})

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
        else: raise NameError('No such name!')
    elif not isinstance(exp, list):
        return exp
    first = exp[0]
    if first == 'quote' or first == '\'':
        return exp[1:]
    elif first == 'if':
        (_, test, t, f) = exp
        return leval(t, local) if leval(test, local) else leval(f, local)
    elif first == 'def':
        (_, var, sub) = exp
        __table[var] = leval(sub, local)
    elif first == 'fn':
        (_, var, sub) = exp
        return Lamfn(var, sub, local)
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
        for i,v in enumerate(self.var):
            local[v] = args[i]
        return leval(self.sub, local)
