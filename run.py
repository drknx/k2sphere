import sys
from engine.lexer import lex
from engine.parser import Parser
from engine.interpreter import Interpreter

def run_file(path):
    with open(path, "r") as f:
        code = f.read()

    tokens = list(lex(code))
    parser = Parser(tokens)
    ast = parser.parse()
    Interpreter().run(ast)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: python run.py <script.k2>")
        sys.exit(1)

    run_file(sys.argv[1])
