'''
    A little LISP written in Python, with many
    thanks to Anton Davydov and Mary Rose Cook.

    @see https://github.com/davydovanton/rlisp
    @see https://github.com/maryrosecook/littlelisp
'''

__author__ = 'Eric Weinstein'


import re
import sys

from functools import reduce
from numbers import Number

class PyLisp(object):
    FLOAT = re.compile('\d*\.\d+')
    INTEGER = re.compile('\d+')

    def __init__(self):
        self.env = {
            '==': lambda args: args[0] == args[1],
            '!=': lambda args: args[0] != args[1],
            '<': lambda args: args[0] < args[1],
            '<=': lambda args: args[0] <= args[1],
            '>': lambda args: args[0] > args[1],
            '>=': lambda args: args[0] >= args[1],
            '+': lambda args: reduce((lambda x, y: x + y), args),
            '-': lambda args: reduce((lambda x, y: x - y), args),
            '*': lambda args: reduce((lambda x, y: x * y), args),
            '/': lambda args: reduce((lambda x, y: x / y), args),
            'car': lambda args: args[0][0],
            'cdr': lambda args: args[0][1:],
            'cons': lambda args: [args[0]] + args[1]
        }

    def run(self, code):
        return self.eval(self.parse(code))

    def parse(self, program):
        return self.read(self.tokenize(program))

    def tokenize(self, chars):
        tokens = re.sub(r'\s\s+', ' ', chars). \
                replace('(', ' ( ').           \
                replace(')', ' ) ').           \
                split(' ')

        return list(filter(lambda x: x != '', tokens))

    def read(self, tokens):
        if not tokens:
            return

        # Grab the first token.
        token = tokens.pop(0)

        if '(' == token:
            token_list = []

            while tokens[0] != ')':
                token_list.append(self.read(tokens))

            # Keep going (since we may have nested lists).
            tokens.pop(0)

            return token_list
        elif ')' == token:
            raise SyntaxError('Unexpected token ")"')
        else:
            return self.atom(token)

    def atom(self, token):
        if self.FLOAT.match(token):
            return float(token)
        elif self.INTEGER.match(token):
            return int(token)
        else:
            return token

    def eval(self, exp, env=None):
        if env is None:
            env = self.env

        if not exp:
            return
        if isinstance(exp, Number):
            return exp
        elif isinstance(exp, str):
            try:
                return env[exp]
            except KeyError:
                return exp
        elif exp[0] == 'quote':
            return exp[1:][0]
        elif exp[0] == 'if':
            _, test, conseq, alt = exp
            test = str(self.eval(test))
            exp = conseq if eval(test, env) else alt
            return exp
        elif exp[0] == 'define':
            _, var, e = exp
            env[var] = self.eval(e)
            return env[var]
        elif exp[0] == 'lambda':
            _, params, body = exp
            return lambda args: self.eval(body, { **env, **dict(zip(params, args)) })
        else:
            fn = exp[0]
            args = exp[1:]
            args = [self.eval(arg, env) for arg in args]
            return env[fn](args)

    def repl(self):
        while True:
            program = input('λ >> ')

            try:
                print(self.run(program))
            except RuntimeError as err:
                print(err)


if __name__ == '__main__':
    pylisp = PyLisp()
    pylisp.repl()
