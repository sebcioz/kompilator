import sys
import ply.yacc as yacc
import TreePrinter as tr
from Parser import Parser


if __name__ == '__main__':

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "example.txt"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    Parser = Parser()
    parser = yacc.yacc(module=Parser)
    text = file.read()

    parsed =  parser.parse(text, lexer=Parser.scanner, debug=1)

    tr.TreePrinter.printAST(parsed)
