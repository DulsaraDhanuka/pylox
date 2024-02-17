from logger import Logger
from scanner import scan_tokens

class Lox():
    def __init__(self):
        self.error = Logger.has_error

    def interpret(self, source: str) -> None:
        tokens = scan_tokens(source)
        self.error = Logger.has_error

