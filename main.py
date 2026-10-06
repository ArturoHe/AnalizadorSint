import sys


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
        '"',
        "'",
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


def isComment(comment):
    return comment.startswith("--")


def isNumber(word):
    try:
        float(word)
        return True
    except ValueError:
        return False


def getPosition(pos=1, row=1, col=1):
    print(pos, row, col)


def printWord(word, row, col):
    if isNumber(word):
        print(f"<tkn_num,{word},{row},{col}>")
    elif isreserved(word):
        print(f"<{word},{row},{col}>")
    elif isSymbol(word):
        print(f"<tkn_{getTokenName(word)},{row},{col}>")
    else:
        print(f"<id,{word},{row},{col}>")


def evaluateInput():

    word = ""
    row = 1
    col = 1

    inputLine = sys.stdin.read()

    arrayLines = inputLine.splitlines()

    arrayWords = []

    for line in arrayLines:
        if isComment(line):
            row += 1
            col = 1
        elif line == "":
            row += 1
            col = 1
        else:
            arrayWords = line.split()

            for i in range(len(arrayWords)):

                printWord(arrayWords[i], row, col)
                col += len(arrayWords[i]) + 1

            row += 1


def main():
    evaluateInput()


if __name__ == "__main__":
    main()
