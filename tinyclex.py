# coding:utf-8

from ply import lex

tokens = (
    'NUMBER',
    'SYMBOL',
    'STRING',
    'VAR',
    'IF',
    'ELSE',
    'RETURN',
    'WHILE',
    'FOR',
    'PRINTLN',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'EQUAL',
    'LT',
    'GT',
    'LPAREN',
    'RPAREN',
    'LBRACE',
    'RBRACE',
    'LBRACKET',
    'RBRACKET',
    'SEMI',
    'COMMA',
)

reserved = {
    'var': 'VAR',
    'if': 'IF',
    'else': 'ELSE',
    'return': 'RETURN',
    'while': 'WHILE',
    'for': 'FOR',
    'println': 'PRINTLN',
}


t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_EQUAL = r'='
t_LT = r'<'
t_GT = r'>'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_SEMI = r';'
t_COMMA = r'\,'


def t_STRING(t):
    r'\"([^\\\n]|(\\.))*?\"'
    t.value = t.value[1:-1]
    return t


def t_NUMBER(t):
    r'\d+'
    try:
         t.value = int(t.value)
    except ValueError:
         print "Number %s is too large!" % t.value
	 t.value = 0
    return t


def t_SYMBOL(t):
    r'[_a-zA-Z][_a-zA-Z0-9]*'
    t.type = reserved.get(t.value, 'SYMBOL')    # Check for reserved words
    return t


t_ignore = " \t\n"


lexer = lex.lex()
