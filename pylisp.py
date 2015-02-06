'''
Date: 2015/02/06-07
Description: Hust.UniqueStudio.Hackday
'''

__table = {}
__specail_forms = {}

def build_table():
    import operator as op
    __table.update({
        '+': op.add, '-': op.sub, '*': op.mul, '/': op.div})

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
            elif ')' == token: stack[-2].append(stack.pop())
            else: stack[-1].append(atom(token))
        return stack.pop()[0]
    except:
        raise SyntaxError('Syntax Error')

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

build_table()
