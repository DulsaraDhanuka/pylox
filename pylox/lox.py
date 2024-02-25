from pylox.logger import Logger
from pylox.scanner import scan_tokens
from pylox.parser import Parser
from pylox.astprinter import AstPrinter

class Lox():
    def __init__(self):
        self.error = Logger.has_error

    def interpret(self, source: str) -> None:
        tokens = scan_tokens(source)
        expression = Parser(tokens).parse()
        self.error = Logger.has_error
        if self.error:
            return
        
        print(AstPrinter().print(expression))

