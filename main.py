import sys
import ply.yacc as yacc
import TreePrinter as tr
from Parser import Parser
from VisibilityChecker import VisibilityChecker
from TypeChecker import TypeChecker
from Interpreter import Interpreter

if __name__ == '__main__':
    sys.setrecursionlimit(10000)

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "example.txt"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    Parser = Parser()
    parser = yacc.yacc(module=Parser)
    text = file.read()

    parsed = parser.parse(text, lexer=Parser.scanner)

    #tr.TreePrinter.printAST(parsed)

    if parsed is not None:
        #print "Compiling {}".format(filename)
        #print

        ch = VisibilityChecker()
        ch.visit(parsed)

        typeChecker = TypeChecker()
        typeChecker.visit(parsed)

        errors = sorted(ch.errors + typeChecker.errors, key=lambda el: el.line)
        warnings = sorted(ch.warnings + typeChecker.warnings, key=lambda el: el.line)
        msg = "successful" if len(errors) == 0 else "failed"

        for error in errors:
            print error
        for warning in warnings:
            print warning

        #print
        #print "Compilation {} ({} errors, {} warnings)".format(msg, len(errors), len(warnings))

        if len(errors) == 0:
            #print
            #print "Output below in stdout"
            #print  "-" * 32

            parsed.accept(Interpreter())
