# coding:utf-8

from ply import yacc
from tinyclex import tokens
from ast import *


precedence = (
    ('right', 'EQUAL'),
    ('left', 'LT', 'GT'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
)


def p_program(p):
    r"""program : 
                | external_definitions"""
    assert len(p) < 3
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = []


def p_external_definitions(p):
    r"""external_definitions : external_definition
                             | external_definitions external_definition"""
    assert len(p) > 1
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[1].append(p[2])
        p[0] = p[1]

   
def p_external_definition_var_1(p) :
    r"external_definition : VAR SYMBOL SEMI"
    p[0] = VarDef(Symbol(p[2]))


def p_external_definition_var_2(p) :
    r"external_definition : VAR SYMBOL EQUAL expr SEMI"
    p[0] = VarDef(Symbol(p[2]), p[4])


# def p_external_definition_var_array(p) :    
#     r"external_definition : VAR SYMBOL LBRACKET expr RBRACKET SEMI"


def p_external_definition_function(p) :
    r"external_definition : SYMBOL parameter_list block"
    p[0] = FuncDef(Symbol(p[1]), p[2], p[3])


def p_parameter_list_1(p):
    r"parameter_list : LPAREN RPAREN"
    p[0] = []


def p_parameter_list_2(p) :
    r"parameter_list : LPAREN symbol_list RPAREN"
    p[0] = p[2]
        

def p_statements(p):
    r"""statements : statement
                   | statements statement"""
    assert len(p) > 1
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[1].append(p[2])
        p[0] = p[1]
    

def p_statement_expr(p) :
    r"""statement : expr SEMI
                  | block"""
    p[0] = Stmt(p[1])


def p_block(p):
    r"block : LBRACE local_vars statements RBRACE"
    p[0] = Block(p[2], p[3])


def p_local_vars(p):
    r"""local_vars : 
                   | VAR symbol_list SEMI"""
    assert len(p) == 1 or len(p) == 4
    if len(p) == 2:
        p[0] = p[2]


def p_symbol_list(p):
    r"""symbol_list : SYMBOL
                    | symbol_list COMMA SYMBOL"""
    assert len(p) > 1
    if len(p) == 2:
        p[0] = [Symbol(p[1])]
    else:
        p[1].append(Symbol(p[3]))
        p[0] = p[1]


def p_statement_if_1(p) :
    r"statement : IF LPAREN expr RPAREN statement"
    p[0] = If(p[3], p[5])


def p_statement_if_2(p) :
    r"statement : IF LPAREN expr RPAREN statement ELSE statement"
    p[0] = If(p[3], p[5], p[7])


def p_statement_return_1(p):
    r"statement : RETURN SEMI"
    p[0] = Return()


def p_statement_return_2(p):
    r"statement : RETURN expr SEMI"
    p[0] = Return(p[2])


def p_statement_while(p) :   
    r"statement : WHILE LPAREN expr RPAREN statement"
    p[0] = While(p[3], p[5])


# def p_statement_for(p) :
#     r"statement : FOR LPAREN expr SEMI expr SEMI expr RPAREN statement"


def p_expr_primary_expr(p) :
    r"expr : primary_expr"
    p[0] = p[1]


def p_expr_assign(p):
    r"expr : SYMBOL EQUAL expr"
    p[0] = Assign(Symbol(p[1]), p[3])


def p_expr_binop(p):
    r"""expr : expr PLUS expr
             | expr MINUS expr
             | expr TIMES expr
             | expr DIVIDE expr
             | expr LT expr
             | expr GT expr"""
    p[0] = BinOp(p[1], p[2], p[3])


# def p_expr_array_assign(p):
#     r"expr : SYMBOL LBRACKET expr RBRACKET EQUAL expr"
#     p[0] = (p[1], p[3], p[6])


def p_primary_expr_symbol(p):
    r"primary_expr : SYMBOL"
    p[0] = Symbol(p[1])


def p_primary_expr_number(p):
    r"primary_expr : NUMBER"
    p[0] = Number(p[1])


def p_primary_expr_string(p):
    r"primary_expr : STRING"
    p[0] = String(p[1])


def p_primary_expr_1(p):
    r"primary_expr : LPAREN expr RPAREN"
    p[0] = p[2]


# def p_primary_expr_array_ref(p) :
#     r"primary_expr : SYMBOL LBRACKET expr RBRACKET"
#     p[0] = (p[1], p[3])
    

def p_primary_expr_funcall_1(p):
    r"primary_expr : SYMBOL LPAREN arg_list RPAREN"
    p[0] = FunCall(Symbol(p[1]), p[3])


def p_primary_expr_funcall_2(p):
    r"primary_expr : SYMBOL LPAREN RPAREN"
    p[0] = FunCall(Symbol(p[1]), [])


def p_primary_expr_println(p):
    r"primary_expr : PRINTLN LPAREN arg_list RPAREN"
    p[0] = PrintLn(p[3])


def p_arg_list(p):
    r"""arg_list : expr
                 | arg_list COMMA expr"""
    assert len(p) > 1
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[1].append(p[3])
        p[0] = p[1]


yacc.yacc(method='LALR')


if __name__ == "__main__":
     while True:
       try:
           s = raw_input('tinyc> ')
       except EOFError:
           break
       if not s:
           continue
       result = yacc.parse(s)
       print result    
