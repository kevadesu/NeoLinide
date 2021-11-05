import tokenize
import sys

def checkKey(dict, key):
    if key in dict:
        return True
    else:
        return False

def lexer(s):
    with open(s, 'rb') as f:
        tokens = tokenize.tokenize(f.readline)
        rtok = []
        ftok = []
        for token in tokens:
            rtok.append(token)
        for raw in rtok:
            linide_types = {}
            linide_types[str(tokenize.NAME)] = "identifier"
            linide_types[str(tokenize.NUMBER)] = "constant"
            linide_types[str(tokenize.STRING)] = "string"
            linide_types[str(tokenize.OP)] = "operator"
            linide_types[str(tokenize.COMMENT)] = "comment"
            """print(f'Keyword: {tokenize.NAME}')
            print(f'Identifier: {tokenize.NAME}')
            print(f'Constant: {tokenize.NUMBER}')
            print(f'String: {tokenize.STRING}')
            print(f'Operator: {tokenize.OP}')
            print(f'Comment: {tokenize.COMMENT}')"""
            if checkKey(linide_types, str(raw.type)):
                #print(linide_types[str(raw.type)])
                special_cases = ["def", "class", "global"]
                #print(raw.string, raw.start, raw.end, raw.string in sp_cases)
                if raw.string in special_cases:
                    ltok = [
                        "keyword",
                        f'{raw.start[0]}.{raw.start[1]}',
                        f'{raw.end[0]}.{raw.end[1]}',
                        raw.string
                    ]
                else:
                    ltok = [
                        linide_types[str(raw.type)],
                        f'{raw.start[0]}.{raw.start[1]}',
                        f'{raw.end[0]}.{raw.end[1]}',
                        raw.string
                    ]
                ftok.append(ltok)
    return ftok