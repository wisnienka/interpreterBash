#!/usr/bin/env python3
import ast
import sys
import ply.lex as lex
import ply.yacc as yacc

reserved = {
    'if': 'IF',
    'then': 'THEN',
    'else': 'ELSE',
    'fi': 'FI',
    '-eq': 'EQ',
    '-ne': 'NE',
    '-gt': 'GT',
    '-lt': 'LT',
}

tokens = [
    'ARG',
    'END',
    'SEMICOLON',
    'PIPE',
    'RIGHT',
    'EQUALS',
    'DOLLAR',
    'L_RECT',
    'R_RECT',
] + list(reserved.values())

t_SEMICOLON = r';'
t_PIPE = r'\|'
t_RIGHT = r'>'
t_EQUALS = r'='
t_DOLLAR = r'\$'
t_L_RECT = r'\['
t_R_RECT = r'\]'
t_ignore = " "

last_program = None


def p_program(t):
    "program : statements"
    global last_program
    last_program = t
    t[0] = t[1]


def t_COMMENT(t):
    r'\#.*\n'
    pass


def t_ARG(t):
    r'[-a-zA-Z0-9_\/]+'
    t.type = reserved.get(t.value,'ARG')    # Check for reserved words
    return t


def t_END(t):
    r'\n'
    t.lexer.lineno += len(t.value)
    return t


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


sys.path.insert(0, "./")


lexer = lex.lex()
context = {}


def p_argument(p):
    '''argument : ARG'''
    p[0] = p[1]


def p_dollar(p):
    '''argument : DOLLAR ARG'''
    p[0] = context[p[2]]


def p_assign(p):
    '''assign : command EQUALS command'''
    p[0] = ast.Assign(p[1], p[3], context)


def p_command(p):
    'command : argument'
    p[0] = ast.Command(p[1], [])


def p_command_with_arg(p):
    '''command : command argument'''
    p[0] = p[1].with_arg(p[2])


def p_statement_pipe(p):
    'command : command PIPE command'
    p[0] = ast.Pipe(p[1], p[3])


def p_if_condition(p):
    '''if_condition : IF L_RECT argument cond_op argument R_RECT'''
    p[0] = ast.IfCondition(p[3], p[4], p[5])


def p_conditional_operator(p):
    '''cond_op : EQ
               | NE
               | LT
               | GT'''
    p[0] = p[1]


def p_if_statement(p):
    '''if_statement : if_condition END THEN END statements END FI'''
    p[0] = ast.IfStatement(p[1], p[5])


def p_if_else_statement(p):
    '''if_else : if_condition END THEN END statements END ELSE END statements END FI'''
    p[0] = ast.IfElseStatement(p[1], p[5], p[9])


def p_statement_redirect_truncate(p):
    'command : command RIGHT argument'
    p[0] = ast.TruncateFile(p[1], p[3])


def p_statement(p):
    '''statement : command
                 | assign
                 | if_statement
                 | if_else'''
    p[0] = p[1]


def p_separator(p):
    """
    separator : SEMICOLON
              | END
              | separator END
              | separator SEMICOLON
    """


def p_statements(p):
    """
    statements : statement
    """
    p[0] = [p[1]]

def p_statements_multiple(p):
    """
    statements : statements separator statement
    """
    p[0] = p[1] + [p[3]]


# Error rule for syntax errors
def p_error(p):
    if p:
        print("Syntax error at '%s'" % p)
    else:
        print("Syntax error at EOF")


yacc.yacc()


import sys

if len(sys.argv) < 2:
    print("USAGE: " + sys.argv[0] + " file.sh")
    sys.exit(1)

file = open(sys.argv[1])
code = file.read()

file.close()

lexer.input(code)

print("----------------LEXER OUTPUT-------------------")
while True:
    tok = lexer.token()
    if not tok:
        break  # No more input
    print(tok.type, tok.value, tok.lineno, tok.lexpos)

print("-------------END OF LEXER OUTPUT---------------")
print("")
print("")
print("")
print("")
print("")


yacc.parse(code, debug = 0)

import subprocess

print("--------EXECUTING COMPILED PROGRAM: -----------")
print("")
print("")

for statement in last_program[0]:
    ast.executeStatement(statement, sys.stdin, sys.stdout, sys.stderr)