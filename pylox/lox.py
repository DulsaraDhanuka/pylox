from pylox.logger import Logger
from pylox.scanner import scan_tokens
from pylox.parser import Parser
from pylox.astprinter import AstPrinter
from pylox.interpreter import Interpreter

class Lox():
    def __init__(self):
        self.error = Logger.has_error
        self.runtime_error = Logger.has_runtime_error
        self.interpreter = Interpreter()

    def clear_errors(self) -> None:
        self.error = False
        self.runtime_error = False
        Logger.has_error = False
        Logger.has_runtime_error = False

    def interpret(self, source: str) -> None:
        tokens = scan_tokens(source)
        self.error = Logger.has_error
        if self.error:
            return
        
        #print(tokens)

        expression = Parser(tokens).parse()
        self.error = Logger.has_error
        if self.error:
            return

        #print("AST", AstPrinter().print(expression))

        self.interpreter.interpret(expression)
        self.runtime_error = Logger.has_runtime_error
        if self.runtime_error:
            return
