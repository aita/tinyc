# coding:utf-8
import operator
from tinycyacc import yacc


class Return(Exception):
    def __init__(self, value):
        self.value = value


class Function(object):
    def __init__(self, params, body):
        self.params = params
        self.body = body


class Variable(object):
    def __init__(self, value):
        self.value = value


def eval_(env, ast):
    for x in ast:
        eval_external_def(env, x)


def eval_external_def(env, ast):
    if ast.type == "funcdef":
        eval_funcdef(env, ast)
    elif ast.type == "vardef":
        eval_vardef(env, ast)
    else:
        raise ValueError("Unknown type: %s" % ast.type)


def eval_funcdef(env, ast):
    env[ast.symbol.value] = Function(ast.parameter_list, ast.block)


def declare_variable(env, ast):
    init_value = ast.expr
    if init_value:
        init_value = eval_expr(init_value)
    env[ast.symbol.value] = Variable(init_value)


def eval_stmt(env, ast):
    if ast.type == "block":
        eval_block(env, ast)
    elif ast.type == "return":
        eval_return(env, ast)
    elif ast.type == "if":
        eval_if(env, ast)
    elif ast.type == "while":
        eval_while(env, ast)
    elif ast.type == "for":
        eval_for(env, ast)
    elif ast.type == "return":
        eval_return(env, ast)
    else:
        eval_expr(env, ast.expr)


def eval_block(env, ast):
    local_env = env.copy()
    local_vars = ast.local_vars
    if local_vars:
        local_env.update({ sym: None for sym in local_vars })
    for stmt in ast.stmts:
        eval_stmt(local_env, stmt)


def eval_return(env, ast):
    raise Return(eval_expr(env, ast.expr))


def eval_if(env, ast):
    if eval_expr(env, ast.cond_expr):
        eval_stmt(env, ast.then_stmt)
    elif ast.else_stmt:
        eval_stmt(env, ast.else_stmt)


def eval_while(env, ast):
    while eval_expr(env, ast.cond_expr):
        eval_stmt(env, ast.stmt)


def eval_expr(env, ast):
    if ast.type == "binop":
        return eval_binop(env, ast)
    elif ast.type == "symbol":
        return env[ast.value]
    elif ast.type == "number":
        return ast.value
    elif ast.type == "string":
        return ast.value
    elif ast.type == "funcall":
        return eval_funcall(env, ast)
    elif ast.type == "assign":
        env[ast.symbol.value] = eval_expr(env, ast.expr)
    elif ast.type == "println":
        eval_println(env, ast)
    else:
        raise ValueError("Unkown type: %s" % ast.type)


def eval_funcall(env, ast):
    function = env[ast.symbol.value]
    return exec_function(env, function, ast.args)


def exec_function(env, function, args):
    assert len(function.params) == len(args)
    local_env = env.copy()
    local_env.update({ sym.value: eval_expr(local_env, arg)
                       for sym, arg in zip(function.params, args) })
    try:
        eval_stmt(local_env, function.body)
    except Return as e:
        return e.value
    

def eval_println(env, ast):
    for x in ast.args:
        result = eval_expr(env, x)
        print result,
    print
            

def eval_binop(env, ast):
    ops = {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '/': operator.div,
        '<': operator.lt,
        '>': operator.gt,
    }
    return ops[ast.op](eval_expr(env, ast.left), eval_expr(env, ast.right))
    

if __name__ == "__main__":
    import sys
    data = sys.stdin.read()
    ast = yacc.parse(data)
    global_env = {}
    eval_(global_env, ast)
    exec_function(global_env, global_env['main'], [])

