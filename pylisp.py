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

def build_table():
    import operator as op
    __table.update({
        '+': op.add, '-': op.sub, '*': op.mul, '/': op.div})

build_table()

# eval

def leval(exp, local={}):
    if isinstance(exp, str):
        if exp in local: return local[exp]
        else: return __table[exp]
    elif not isinstance(exp, list):
        return exp
    first = exp[0]
    if first == 'quote' or first == '\'':
        return x[1:]
    elif first == 'if':
        (_, test, t, f) = exp
        return leval(t, local) if leval(test, local) else leval(f, local)
    elif first == 'def':
        (_, var, sub) = exp
        __table[var] = leval(sub, local)
    elif first == 'fn':
        pass
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
                print parse(source)
                try : print leval(parse(source))
                except Exception, e: print e
            elif paren < 0:
                print 'Error: unmacthed parentheis!'
            pro = prompt
            source = ''
        else:
            pro = '.'*len(prompt[:-2]) + '=>' + ' '*paren*2

