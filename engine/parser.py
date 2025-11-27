class NumberNode:
    def __init__(self, value):
        self.value = value

class StringNode:
    def __init__(self, value):
        self.value = value

class VarNode:
    def __init__(self, name):
        self.name = name

class BinOpNode:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class AssignNode:
    def __init__(self, name, expr):
        self.name = name
        self.expr = expr

class BlockNode:
    def __init__(self, statements):
        self.statements = statements

class IfNode:
    def __init__(self, cond, then_block, else_block):
        self.cond = cond
        self.then_block = then_block
        self.else_block = else_block

class WhileNode:
    def __init__(self, cond, body):
        self.cond = cond
        self.body = body

class FuncDefNode:
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body

class ReturnNode:
    def __init__(self, expr):
        self.expr = expr

class CallNode:
    def __init__(self, name, args):
        self.name = name
        self.args = args

class ImportNode:
    def __init__(self, name):
        self.name = name


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.i = 0

    def peek(self):
        return self.tokens[self.i] if self.i < len(self.tokens) else ("EOF", None)

    def advance(self):
        self.i += 1

    def match(self, *types):
        tok_type, value = self.peek()
        if tok_type in types:
            self.advance()
            return value
        return None

    def consume(self, tok, msg):
        tok_type, value = self.peek()
        if tok_type != tok:
            raise Exception(msg)
        self.advance()
        return value

    def parse(self):
        statements = []
        while self.peek()[0] != "EOF":
            stmt = self.statement()
            if stmt:
                statements.append(stmt)
        return BlockNode(statements)

    def statement(self):
        tok_type, _ = self.peek()

        if tok_type == "IMPORT":
            return self.import_stmt()

        if tok_type == "FN":
            return self.func_def()

        if tok_type == "IF":
            return self.if_stmt()

        if tok_type == "WHILE":
            return self.while_stmt()

        if tok_type == "RETURN":
            return self.return_stmt()

        return self.expr_stmt()

    def import_stmt(self):
        self.consume("IMPORT", "expected import")
        name = self.consume("STRING", "expected library name")
        return ImportNode(name.strip("\""))

    def func_def(self):
        self.consume("FN", "expected fn")
        name = self.consume("IDENT", "expected function name")
        self.consume("LPAREN", "expected (")
        params = []
        while not self.match("RPAREN"):
            p = self.consume("IDENT", "expected parameter")
            params.append(p)
            self.match("COMMA")
        self.consume("THEN", "expected then")
        body = self.block()
        self.consume("END", "expected end")
        return FuncDefNode(name, params, body)

    def if_stmt(self):
        self.consume("IF", "expected if")
        self.consume("LPAREN", "expected (")
        cond = self.expression()
        self.consume("RPAREN", "expected )")
        self.consume("THEN", "expected then")
        then_block = self.block()

        else_block = None
        if self.match("ELSE"):
            self.consume("THEN", "expected then")
            else_block = self.block()

        self.consume("END", "expected end")
        return IfNode(cond, then_block, else_block)

    def while_stmt(self):
        self.consume("WHILE", "expected while")
        self.consume("LPAREN", "expected (")
        cond = self.expression()
        self.consume("RPAREN", "expected )")
        self.consume("THEN", "expected then")
        body = self.block()
        self.consume("END", "expected end")
        return WhileNode(cond, body)

    def return_stmt(self):
        self.consume("RETURN", "expected return")
        expr = self.expression()
        return ReturnNode(expr)

    def expr_stmt(self):
        expr = self.expression()
        return expr

    def block(self):
        statements = []
        while self.peek()[0] not in ("END", "ELSE", "EOF"):
            statements.append(self.statement())
        return BlockNode(statements)

    def expression(self):
        return self.assignment()

    def assignment(self):
        expr = self.binary()
        if self.match("EQ"):
            value = self.expression()
            if isinstance(expr, VarNode):
                return AssignNode(expr.name, value)
            raise Exception("invalid assignment")
        return expr

    def binary(self):
        left = self.primary()
        while (op := self.peek()[0]) in ("PLUS", "MINUS", "STAR", "SLASH", "EQEQ", "NEQ", "LT", "GT", "LE", "GE"):
            self.advance()
            right = self.primary()
            left = BinOpNode(left, op, right)
        return left

    def primary(self):
        tok_type, value = self.peek()

        if tok_type == "NUMBER":
            self.advance()
            return NumberNode(value)

        if tok_type == "STRING":
            self.advance()
            return StringNode(value)

        if tok_type == "IDENT":
            self.advance()
            name = value
            if self.match("LPAREN"):
                args = []
                while not self.match("RPAREN"):
                    args.append(self.expression())
                return CallNode(name, args)
            return VarNode(name)

        raise Exception(f"Unexpected token {tok_type}")
