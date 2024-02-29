import string
from typing import List
from pylox.tokentypes import TokenType
from pylox.logger import Logger
from pylox.token import Token

# TODO: Rewrite the scanner using classes
def scan_tokens(source: str) -> List[Token]:
    tokens: List[Token] = []
    start: int = 0
    current: int = 0
    line: int = 1
    while current < len(source):
        start = current
        current, line, token = scan_token(source, start, current, line)
        if token is not None:
            tokens += [token]
    tokens += [Token(TokenType.EOF, "", None, line)]
    return tokens

def scan_token(source: str, start: int, current: int, line: int) -> (int, int, Token):
    c = source[current]
    c_after = source[current+1] if current+1 < len(source) else '\0'
    current += 1

    if c == '(':
        return current, line, create_token(TokenType.LEFT_PAREN, source, start, current, line)
    elif c == ')':
        return current, line, create_token(TokenType.RIGHT_PAREN, source, start, current, line)
    elif c == '{':
        return current, line, create_token(TokenType.LEFT_BRACE, source, start, current, line)
    elif c == '}':
        return current, line, create_token(TokenType.RIGHT_BRACE, source, start, current, line)
    elif c == ',':
        return current, line, create_token(TokenType.COMMA, source, start, current, line)
    elif c == '.':
        return current, line, create_token(TokenType.DOT, source, start, current, line)
    elif c == '-':
        return current, line, create_token(TokenType.MINUS, source, start, current, line)
    elif c == '+':
        return current, line, create_token(TokenType.PLUS, source, start, current, line)
    elif c == ';':
        return current, line, create_token(TokenType.SEMICOLON, source, start, current, line)
    elif c == '*':
        return current, line, create_token(TokenType.STAR, source, start, current, line)
    elif c == '!':
        if c_after == '=':
            return current+1, line, create_token(TokenType.BANG_EQUAL, source, start, current+1, line)
        else:
            return current, line, create_token(TokenType.BANG, source, start, current, line)
    elif c == '=':
        if c_after == '=':
            return current+1, line, create_token(TokenType.EQUAL_EQUAL, source, start, current+1, line)
        else:
            return current, line, create_token(TokenType.EQUAL, source, start, current, line)
    elif c == '<':
        if c_after == '=':
            return current+1, line, create_token(TokenType.LESS_EQUAL, source, start, current+1, line)
        else:
            return current, line, create_token(TokenType.LESS, source, start, current, line)
    elif c == '>':
        if c_after == '=':
            return current+1, line, create_token(TokenType.GREATER_EQUAL, source, start, current+1, line)
        else:
            return current, line, create_token(TokenType.GREATER, source, start, current, line)
    elif c == '/':
        if c_after == '/':
            current += 1
            while len(source) > current and source[current] != '\n':
                current += 1
            return current, line, None
        elif c_after == '*':
            current += 1
            nested = 0
            while len(source) > current+1 and not (source[current] == '*' and source[current+1] == '/' and nested == 0):
                if source[current] == '/' and source[current+1] == '*':
                    nested += 1
                    current += 1
                elif source[current] == '*' and source[current+1] == '/':
                    nested -= 1
                    current += 1
                current += 1
            return current+2, line, None
        else:
            return current, line, create_token(TokenType.SLASH, source, start, current, line)
    elif c == '"':
        return process_string(source, start, current, line)
    elif c == ' ' or c == '\r' or c == '\t':
        return current, line, None
    elif c == '\n':
        return current, line+1, None
    elif is_digit(c):
        return process_number(source, start, current, line)
    elif is_alpha(c):
        return process_identifier(source, start, current, line)
    else:
        Logger.error("Unexpected character.", line=line)
        return current, line, None

def process_string(source: str, start: int, current: int, line: int) -> (int, int, Token):
    start_line = line
    start = current
    while current < len(source) and source[current] != '"':
        if source[current] == "\n": line += 1
        current += 1
    if current >= len(source):
        Logger.error("Unterminated string literal", line=start_line)
        return current, line, None
    return current+1, line, create_token(TokenType.STRING, source, start-1, current+1, line, literal=source[start:current])

def is_digit(c: str) -> bool: return c[0] in string.digits

def process_number(source: str, start: int, current: int, line: int) -> (int, int, Token):
    start = current - 1
    while current < len(source) and is_digit(source[current]): current += 1

    if current+1 < len(source) and source[current] == "." and is_digit(source[current+1]):
        current += 1
        while current < len(source) and is_digit(source[current]): current += 1

    return current, line, create_token(TokenType.NUMBER, source, start, current, line, literal=float(source[start:current]))

def is_alpha(c: str) -> bool: return c[0] in string.ascii_letters + '_'

def is_alphanumeric(c: str) -> bool: return is_digit(c) or is_alpha(c)

def process_identifier(source: str, start: int, current: int, line: int) -> (int, int, Token):
    start = current - 1
    while current < len(source) and is_alphanumeric(source[current]): current += 1

    keywords = {}
    keywords['and'] = TokenType.AND
    keywords['class'] = TokenType.CLASS
    keywords['else'] = TokenType.ELSE
    keywords['false'] = TokenType.FALSE
    keywords['function'] = TokenType.FUNCTION
    keywords['if'] = TokenType.IF
    keywords['nil'] = TokenType.NIL
    keywords['or'] = TokenType.OR
    keywords['print'] = TokenType.PRINT
    keywords['return'] = TokenType.RETURN
    keywords['super'] = TokenType.SUPER
    keywords['this'] = TokenType.THIS
    keywords['true'] = TokenType.TRUE
    keywords['var'] = TokenType.VAR
    keywords['while'] = TokenType.WHILE

    text = source[start:current]
    tokenType = keywords.get(text, TokenType.IDENTIFIER)
    return current, line, create_token(tokenType, source, start, current, line)

def create_token(tokentype: TokenType, source: str, start: int, current: int, line: int, literal=None) -> Token:
    text = source[start:current]
    return Token(tokentype, text, literal, line)

