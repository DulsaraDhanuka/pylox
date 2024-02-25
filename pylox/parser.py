from pylox.scanner import Token
from pylox.tokentypes import TokenType
from pylox.expr import Expr, Binary, Unary, Literal, Grouping
from pylox.logger import Logger

class ParserError(RuntimeError): pass
class Parser(object):
    def __init__(self, tokens: list[Token]) -> None:
        self.tokens: list[Token] = tokens
        self.current = 0

    def parse(self) -> Expr:
        try:
            return self.expression()
        except ParserError as e:
            return None

    def expression(self) -> Expr:
        return self.equality()

    def equality(self) -> Expr:
        expr = self.comparison()
        while self._match(TokenType.EQUAL_EQUAL, TokenType.BANG_EQUAL):
            op = self._consume()
            right = self.comparison()
            expr = Binary(expr, op, right)
        return expr

    def comparison(self) -> Expr:
        expr = self.term()
        while self._match(TokenType.GREATER, TokenType.LESS, TokenType.GREATER_EQUAL, TokenType.LESS_EQUAL):
            op = self._consume()
            right = self.term()
            expr = Binary(expr, op, right)
        return expr

    def term(self) -> Expr:
        expr = self.factor()
        while self._match(TokenType.PLUS, TokenType.MINUS):
            op = self._consume()
            right = self.factor()
            expr = Binary(expr, op, right)
        return expr
    
    def factor(self) -> Expr:
        expr = self.unary()
        while self._match(TokenType.SLASH, TokenType.STAR):
            op = self._consume()
            right = self.unary()
            expr = Binary(expr, op, right)
        return expr
   
    def unary(self) -> Expr:
        if self._match(TokenType.BANG, TokenType.MINUS):
            return Unary(self._consume(), self.unary())
        return self.primary()

    def primary(self) -> Expr:
        if self._match(TokenType.TRUE): return Literal(True)
        if self._match(TokenType.FALSE): return Literal(False)
        if self._match(TokenType.NIL): return Literal(None)

        if self._match(TokenType.STRING, TokenType.NUMBER): return Literal(self._consume().literal)

        if self._match(TokenType.LEFT_PAREN):
            expr = self.expression()
            tok = self._consume()
            if tok.tokentype == TokenType.RIGHT_PAREN:
                return Grouping(expr)
            else:
                # TODO: Print error "Expected ')' after expression."
                Logger.error("Expect ')' after expression.", token=tok)
                raise ParserError()

        Logger.error("Expect expression.", token=self._peek())
        raise ParserError()

    def synchronize(self) -> None:
        while not self._is_at_end():
            if self._peek().tokentype == TokenType.SEMICOLOR: 
                self._consume()
                return
            if self._match(TokenType.CLASS, TokenType.FUNCTION, TokenType.VAR, TokenType.FOR, TokenType.IF, TokenType.WHILE, TokenType.PRINT, TokenType.RETURN):
                return
            self._consume()
        return

    def _match(self, *types) -> bool: 
        for _type in types:
            if self._peek().tokentype == _type:
                return True
        return False

    def _consume(self) -> Token:
        if self._is_at_end(): return None

        self.current += 1
        return self.tokens[self.current-1]

    def _peek(self) -> Token:
        if self._is_at_end(): return None
        return self.tokens[self.current]

    def _is_at_end(self) -> bool:
        return self.tokens[self.current].tokentype == TokenType.EOF

