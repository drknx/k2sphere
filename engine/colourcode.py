# colour is fun
from engine.lexer import Lexer
from engine.parser import Parser
from engine.interpreter import Interpreter

# ANSI color map
COLOR_MAP = {
    "if": 31,
    "else": 32,
    "while": 33,
    "function": 34,
    "output": 35,
    "get": 36,
    "then": 33,
    "end": 32
}

interpreter = Interpreter()

print("K2Sphere REPL with keyword colors")
print("type exit to quit")

while True:
    line = input(">>> ")
    if line.strip() == "exit":
        break

    # tokenize each word for coloring
    words = line.split(" ")
    colored_line = ""
    for w in words:
        color = COLOR_MAP.get(w, 37)  # default white
        colored_line += f"\033[{color}m{w}\033[0m "
    
    print(colored_line.strip())

    try:
        tokens = Lexer(line).tokenize()
        tree = Parser(tokens).parse()
        interpreter.run(tree)
    except Exception as e:
        print(f"\033[31mError: {e}\033[0m")
