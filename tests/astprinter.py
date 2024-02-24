import os
import sys
sys.path.append(os.getcwd())

from pylox.astprinter import AstPrinter
from pylox.expr import Binary, Unary, Grouping, Literal
from pylox.scanner import Token
from pylox.tokentypes import TokenType

expression = Binary(
        Unary(
            Token(TokenType.MINUS, "-", None, 1), 
            Literal(123),
            ),
        Token(TokenType.STAR, "*", None, 1),
        Grouping(Literal(12.22))
        )

print(AstPrinter().print(expression))
