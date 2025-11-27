from engine.lexer import lex
from engine.parser import Parser, NumberNode, StringNode, VarNode, BinOpNode, AssignNode, \
    BlockNode, IfNode, WhileNode, FuncDefNode, ReturnNode, CallNode, ImportNode


class ReturnSignal(Exception):
    def __init__(self, value):
        self.value = value


class Interpreter:
    def __init__(self):
        self.env = {
            "print": lambda *a: print(*a)
        }
        self.functions = {}

    def run(self, ast):
        return self.exec_block(ast)

    def exec_block(self, block):
        result = None
        for stmt in block.statements:
            result = self.exec(stmt)
        return result

    def exec(self, node):

        if isinstance(node, NumberNode):
            return node.value

        if isinstance(node, StringNode):
            return node.value.strip('"')

        if instanceof := isinstance(node, VarNode):
            return self.env.get(node.name, None)

        if isinstance(node, AssignNode):
            val = self.exec(node.expr)
            self.env[node.name] = val
            return val

        if isinstance(node, BinOpNode):
            l = self.exec(node.left)
            r = self.exec(node.right)
            return self.eval_op(node.op, l, r)

        if isinstance(node, BlockNode):
            return self.exec_block(node)

        if isinstance(node, IfNode):
            if self.exec(node.cond):
                return self.exec(node.then_block)
            elif node.else_block:
                return self.exec(node.else_block)
            return None

        if isinstance(node, WhileNode):
            while self.exec(node.cond):
                self.exec(node.body)
            return None

        if isinstance(node, FuncDefNode):
            self.functions[node.name] = node
            return None

        if isinstance(node, CallNode):
            return self.exec_call(node)

        if isinstance(node, ReturnNode):
            val = self.exec(node.expr)
            raise ReturnSignal(val)

        if isinstance(node, ImportNode):
            return self.exec_import(node)

        raise Exception("Unknown AST node")

    def eval_op(self, op, l, r):
        return {
            "PLUS": l + r,
            "MINUS": l - r,
            "STAR": l * r,
            "SLASH": l / r,
            "EQEQ": l == r,
            "NEQ": l != r,
            "LT": l < r,
            "GT": l > r,
            "LE": l <= r,
            "GE": l >= r,
        }[op]

    def exec_call(self, node):
        if node.name in self.env and callable(self.env[node.name]):
            args = [self.exec(a) for a in node.args]
            return self.env[node.name](*args)

        func = self.functions.get(node.name)
        if func is None:
            raise Exception(f"Undefined function {node.name}")

        local = {}
        for pname, arg in zip(func.params, node.args):
            local[pname] = self.exec(arg)

        previous = self.env
        self.env = {**previous, **local}

        try:
            self.exec(func.body)
        except ReturnSignal as r:
            self.env = previous
            return r.value

        self.env = previous
        return None

    def exec_import(self, node):
        filename = f"./libs/{node.name}.k2"
        with open(filename, "r") as f:
            code = f.read()

        tokens = list(lex(code))
        ast = Parser(tokens).parse()
        self.run(ast)
