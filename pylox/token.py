from pylox.tokentypes import TokenType

class Token(object):
    def __init__(self, tokentype: TokenType, lexeme: str, literal, line: int) -> None:
        self.tokentype: TokenType = tokentype
        self.lexeme: str = lexeme
        self.literal = literal
        self.line = line
    
    def __repr__(self):
        return f"{self.tokentype} {self.lexeme} {self.literal}"
