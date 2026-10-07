import sys

DIGITS = "0123456789"


def isreserved(word):
    reservedWords = [
        "and",
        "break",
        "do",
        "else",
        "elseif",
        "end",
        "false",
        "for",
        "function",
        "global",
        "goto",
        "if",
        "in",
        "local",
        "nil",
        "not",
        "or",
        "repeat",
        "return",
        "then",
        "true",
        "until",
        "while",
        "print",
        "error",
        "warn",
        "pcall",
        "xpcall"
    ]

    return word in reservedWords


def isSymbol(symbol):
    symbols = [
        "&",
        "|",
        "~",
        ">>",
        "<<",
        ";",
        ":",
        ",",
        ".",
        "::",
        "..",
        "...",
        "{",
        "}",
        "[",
        "]",
        "(",
        ")",
        "#",
        "+",
        "-",
        "*",
        "/",
        "//",
        "^",
        "%",
        "==",
        "~=",
        "<=",
        ">=",
        ">",
        "<",
        "=",
    ]

    return symbol in symbols


def getTokenName(word):
    tokens = {
        "&": "bit_and",
        "|": "bit_or",
        "~": "bitex_or",
        ">>": "right_shift",
        "<<": "left_shift",
        ";": "semicolon",
        ":": "colon",
        ",": "comma",
        ".": "period",
        "::": "goto",
        "..": "concat",
        "...": "varargs",
        "{": "opening_key",
        "}": "closing_key",
        "[": "opening_bra",
        "]": "closing_bra",
        "(": "opening_par",
        ")": "closing_par",
        "#": "length",
        "+": "plus",
        "-": "minus",
        "*": "times",
        "/": "div",
        "//": "floor_div",
        "^": "power",
        "%": "mod",
        "==": "equal",
        "~=": "neq",
        "<=": "leq",
        ">=": "geq",
        ">": "greater",
        "<": "less",
        "=": "assign",
    }

    tokenName = tokens[word]
    return tokenName


def isLetter(c):
    return c == "_" or ("a" <= c <= "z") or ("A" <= c <= "Z")


def isDigit(c):
    return len(c) == 1 and c in DIGITS


def isNumber(word):
    parts = word.split(".")
    if len(parts) > 2:
        return False
    return all(p != "" and all(isDigit(c) for c in p) for p in parts)


def isComment(texto, pos):
    if texto.startswith("--[[", pos):
        return 2
    if texto.startswith("--", pos):
        return 1
    return 0



def peek(texto, pos):
    return texto[pos] if pos < len(texto) else ""


def advance(texto, pos, row, col, n=1):
    for _ in range(n):
        if texto[pos] == "\n":
            row += 1
            col = 1
        else:
            col += 1
        pos += 1
    return pos, row, col



def identifierLength(texto, pos):
    n = 0
    while isLetter(peek(texto, pos + n)) or isDigit(peek(texto, pos + n)):
        n += 1
    return n


def numberLength(texto, pos):
    n = 0
    while isDigit(peek(texto, pos + n)):
        n += 1
    if peek(texto, pos + n) == "." and isDigit(peek(texto, pos + n + 1)):
        n += 1
        while isDigit(peek(texto, pos + n)):
            n += 1
    return n


def symbolLength(texto, pos):
    n = 0

    while pos + n < len(texto) and isSymbol(texto[pos : pos + n + 1]):
        n += 1
    return n


def stringEnd(texto, pos):

    quote = texto[pos]
    i = pos + 1
    while i < len(texto):
        ch = texto[i]
        if ch == "\n":
            return -1
        if ch == "\\": 
            i += 2
            continue
        if ch == quote:
            return i
        i += 1
    return -1


def skipComment(texto, pos, row, col, kind):
    pos, row, col = advance(texto, pos, row, col, 2)  # consume "--"
    if kind == 2:
        pos, row, col = advance(texto, pos, row, col, 2)  # consume "[["
        while pos < len(texto) and not texto.startswith("]]", pos):
            pos, row, col = advance(texto, pos, row, col)
        if pos < len(texto):
            pos, row, col = advance(texto, pos, row, col, 2)  # consume "]]"
    else:
        while pos < len(texto) and texto[pos] != "\n":
            pos, row, col = advance(texto, pos, row, col)
    return pos, row, col



def printWord(word, row, col):
    if isNumber(word):
        print(f"<tkn_num,{word},{row},{col}>")
    elif isreserved(word):
        print(f"<{word},{row},{col}>")
    elif isSymbol(word):
        print(f"<tkn_{getTokenName(word)},{row},{col}>")
    else:
        print(f"<id,{word},{row},{col}>")


def printString(word, row, col):
    print(f"<tkn_str,{word},{row},{col}>")


def printError(row, col):
    print(f">>> Error lexico (linea: {row}, posicion: {col})")


def evaluateInput():

    texto = sys.stdin.read()

    pos = 0
    row = 1
    col = 1

    while pos < len(texto):

        c = texto[pos]

        if c in " \t\r\n":
            pos, row, col = advance(texto, pos, row, col)

        elif isComment(texto, pos) != 0:  # antes que símbolos: "--" no es "-" "-"
            kind = isComment(texto, pos)
            pos, row, col = skipComment(texto, pos, row, col, kind)

        elif isLetter(c):
            n = identifierLength(texto, pos)
            printWord(texto[pos : pos + n], row, col)
            pos, row, col = advance(texto, pos, row, col, n)

        elif isDigit(c):
            n = numberLength(texto, pos)
            printWord(texto[pos : pos + n], row, col)
            pos, row, col = advance(texto, pos, row, col, n)

        elif c == '"' or c == "'":
            end = stringEnd(texto, pos)
            if end == -1:
                printError(row, col)
                return
            printString(texto[pos + 1 : end], row, col)
            pos, row, col = advance(texto, pos, row, col, end - pos + 1)

        else:
            n = symbolLength(texto, pos)
            if n == 0:
                printError(row, col)
                return
            printWord(texto[pos : pos + n], row, col)
            pos, row, col = advance(texto, pos, row, col, n)


def main():
    evaluateInput()


if __name__ == "__main__":
    main()
