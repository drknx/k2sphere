import re
import json
import os

# load custom keywords
KEYWORDS_PATH = os.path.join(os.path.dirname(__file__), "..", "config", "keywords.json")
with open(KEYWORDS_PATH, "r") as f:
    KEYWORDS = json.load(f)

# token specifications (dynamic keywords)
TOKENS = [
    ("NUMBER", r"\d+"),
    ("STRING", r"\".*?\""),
    ("IDENT", r"[A-Za-z_][A-Za-z0-9_]*"),

    ("PLUS", r"\+"),
    ("MINUS", r"-"),
    ("STAR", r"\*"),
    ("SLASH", r"/"),
    ("EQ", r"="),
    ("EQEQ", r"=="),
    ("NEQ", r"!="),
    ("LT", r"<"),
    ("GT", r">"),
    ("LE", r"<="),
    ("GE", r">="),

    ("LPAREN", r"\("),
    ("RPAREN", r"\)"),

    # dynamic syntax tokens
    ("IF", rf"{KEYWORDS['if']}\b"),
    ("ELSE", rf"{KEYWORDS['else']}\b"),
    ("WHILE", rf"{KEYWORDS['while']}\b"),
    ("FN", rf"{KEYWORDS['fn']}\b"),
    ("RETURN", rf"{KEYWORDS['return']}\b"),
    ("IMPORT", rf"{KEYWORDS['import']}\b"),

    ("THEN", rf"{KEYWORDS['then']}\b"),
    ("END", rf"{KEYWORDS['end']}\b"),

    ("NEWLINE", r"\n"),
    ("SKIP", r"[ \t]+"),
    ("MISMATCH", r"."),
]

master_regex = "|".join(f"(?P<{name}>{regex})" for name, regex in TOKENS)


def lex(code):
    for m in re.finditer(master_regex, code):
        token_type = m.lastgroup
        value = m.group()

        if token_type == "NUMBER":
            yield ("NUMBER", int(value))
        elif token_type == "STRING":
            yield ("STRING", value)
        elif token_type in ("IDENT", "IF", "ELSE", "WHILE", "FN", "RETURN", "IMPORT", "THEN", "END"):
            yield (token_type, value)
        elif token_type == "NEWLINE":
            yield ("NEWLINE", None)
        elif token_type == "SKIP":
            continue
        elif token_type == "MISMATCH":
            raise Exception(f"Illegal character: {value}")
        else:
            yield (token_type, value)
