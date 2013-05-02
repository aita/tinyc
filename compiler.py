# coding:utf-8
# import operator
from tinycyacc import yacc
# from collections import OrderedDict


def compile(fp, ast):
    env = {}
    for x in ast:
        compile_external_def(fp, env, x)


def compile_external_def(fp, env, ast):
    if ast.type == "funcdef":
        compile_funcdef(fp, env, ast)
    elif ast.type == "vardef":
        compile_vardef(fp, env, ast)
    else:
        raise ValueError("Unknown type: %s" % ast.type)


def compile_vardef(fp, env, ast):
    # init_value = None
    # if ast.expr:
    #     init_value = compile_expr(env, ast.expr)
    # env[ast.symbol] = init_value
    pass


def compile_funcdef(fp, env, ast):
    local_env = env.copy()
    for idx, symbol in enumerate(ast.parameter_list):
        local_env[symbol.value] = ("ARG", idx)
    fp.write("ENTRY %s\n" % ast.symbol.value)
    fp.write("FRAME %s\n" % 0)
    compile_stmt(fp, local_env, ast.block)
    fp.write("RET\n")


def compile_stmt(fp, env, ast):
    if ast.type == "block":
        compile_block(fp, env, ast)
    elif ast.type == "return":
        # compile_return(fp, env, ast)
        if ast.expr:
            compile_expr(fp, env, ast.expr)
        fp.write("RET\n")
    elif ast.type == "if":
        compile_if(fp, env, ast)
    elif ast.type == "while":
        compile_while(fp, env, ast)
    elif ast.type == "for":
        compile_for(fp, env, ast)
    else:
        compile_expr(fp, env, ast.expr)
        fp.write("POP\n")
    

def compile_block(fp, env, ast):
    local_env = env.copy()
    local_vars = ast.local_vars or []
    for idx, symbol in enumerate(local_vars):
        local_env[symbol.value] =  ("LOC", idx)
    # print local_vars
    for stmt in ast.stmts:
        compile_stmt(fp, local_env, stmt)

        
def compile_expr(fp, env, ast):
    if ast.type == "number":
        fp.write("PUSHI %s\n" % ast.value)
    elif ast.type == "symbol":
        vartype, pos = env[ast.value]
        if vartype == "ARG":
            op = "LOADA"
        else:
            op = "LOADI"
        fp.write("%s %s\n" % (op, pos))
    elif ast.type == "binop":
        compile_binop(fp, env, ast)
    elif ast.type == "funcall":
        compile_funcall(fp, env, ast)
    elif ast.type == "assign":
        compile_expr(fp, env, ast.expr)
        vartype, pos = env[ast.symbol.value]
        if vartype == "ARG":
            op = "STOREA"
        else:
            op = "STOREI"
        fp.write("%s %s\n" % (op, pos))
    elif ast.type == "println":
        for x in ast.args[1:]:
            compile_expr(fp, env, x)
        fp.write("PRINTLN \"%s\"\n" % ast.args[0].value)
    else:
        raise ValueError("Unkown type: %s" % ast.type)


def compile_binop(fp, env, ast):
    ops = {
        '+': "ADD",
        '-': "SUB",
        '*': "MUL",
        '/': "DIV",
        '<': "LT",
        '>': "GT",
    }
    compile_expr(fp, env, ast.left)
    compile_expr(fp, env, ast.right)
    fp.write("%s\n" % ops[ast.op])


def compile_funcall(fp, env, ast):
    args = ast.args
    for arg in reversed(args):
        compile_expr(fp, env, arg)
    fp.write("CALL %s\n" % ast.symbol.value)
    fp.write("POPR %s\n" % len(args))
    


if __name__ == "__main__":
    import sys
    data = sys.stdin.read()
    ast = yacc.parse(data)
    compile(sys.stdout, ast)
