# coding:utf-8

class AST(object):
    pass


class Expr(AST):
    pass


class FuncDef(AST):
    def __init__(self, symbol, parameter_list, block):
        self.type = "funcdef"
        self.symbol = symbol
        self.parameter_list = parameter_list
        self.block = block

    def __repr__(self):
        return "FuncDef(%s, %s, %s)" % (self.symbol,
                                        self.parameter_list,
                                        self.block)


class VarDef(AST):
    def __init__(self, symbol, expr=None):
        self.type = "vardef"
        self.symbol = symbol
        self.expr = expr

    def __repr__(self):
        if self.expr:
            return "VarDef(%s, %s)" % (self.symbol, self.expr)
        return "VarDef(%s)" % self.symbol


class Block(AST):
    def __init__(self, local_vars, stmts):
        self.type = "block"
        self.local_vars = local_vars
        self.stmts = stmts

    def __repr__(self):
        if self.local_vars:
            return "Block(%s, %s)" % (self.local_vars,
                                      self.stmts)
        return "Block(%s)" % self.stmts


class Stmt(AST):
    def __init__(self, expr):
        self.type = "stmt"
        self.expr = expr

    def __repr__(self):
        return "Stmt(%s)" % self.expr


class If(Stmt):
    def __init__(self, cond_expr, then_stmt, else_stmt=None):
        self.type = "if"
        self.cond = cond_expr
        self.then_stmt = then_stmt
        self.else_stmt = else_stmt

    def __repr__(self):
        if self.else_stmt:
            return "If(%s, %s, %s)" % (self.cond_expr,
                                       self.then_stmt, self.else_stmt)
        return "If(%s, %s)" % (self.cond, self.then_stmt)


class While(Stmt):
    def __init__(self, cond_expr, stmt):
        self.type = "while"
        self.cond_expr = cond_expr
        self.stmt = stmt

    def __repr__(self):
        return "While(%s, %s)" % (self.cond_expr, self.stmt)


class Return(Stmt):
    def __init__(self, expr):
        self.type = "return"
        self.expr = expr

    def __repr__(self):
        if self.expr:
            return "Return(%s)" % self.expr
        return "Return()"


class BinOp(Expr):
    def __init__(self, left, op, right):
        self.type = "binop"
        self.left = left
        self.op = op
        self.right = right

    def __repr__(self):
        return "BinOp(%s, %s, %s)" % (self.left, self.op, self.right)


class Assign(Expr):
    def __init__(self, symbol, expr):
        self.type = "assign"
        self.symbol = symbol
        self.expr = expr

    def __repr__(self):
        return "Assign(%s, %s)" % (self.symbol, self.expr)


class FunCall(Expr):
    def __init__(self, symbol, args=None):
        self.type = "funcall"
        self.symbol = symbol
        self.args = args

    def __repr__(self):
        if self.args:
            return "FunCall(%s, %s)" % (self.symbol, self.args)
        return "FunCall(%s)" % self.symbol


class Symbol(Expr):
    def __init__(self, value):
        self.type = "symbol"
        self.value = value

    def __repr__(self):
        return "Symbol(%s)" % self.value


class Number(Expr):
    def __init__(self, value):
        self.type = "number"
        self.value = value

    def __repr__(self):
         return "Number(%s)" % self.value


class String(Expr):
    def __init__(self, value):
        self.type = "string"
        self.value = value

    def __repr__(self):
        return "String(\"%s\")" % self.value


class PrintLn(Expr):
    def __init__(self, args):
        self.type = "println"
        self.args = args

    def __repr__(self):
        return "PrintLn(%s)" % self.args
