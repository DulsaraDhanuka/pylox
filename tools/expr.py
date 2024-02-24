from scanner import Token
from abc import ABC, abstractmethod

class Visitor(ABC):
    @abstractmethod
    def visit_binary_expr(self, expr: Binary) -> object:
        pass
    @abstractmethod
    def visit_unary_expr(self, expr: Unary) -> object:
        pass
    @abstractmethod
    def visit_grouping_expr(self, expr: Grouping) -> object:
        pass
    @abstractmethod
    def visit_literal_expr(self, expr: Literal) -> object:
        pass
class Expr(ABC):
    @abstractmethod
    def accept(self, visitor: Visitor) -> object:
        pass
class Binary(object):
    def __init__(self, left: Expr, operator: Token, right: Expr) -> None:
        self.left: Expr = left
        self.operator: Token = operator
        self.right: Expr = right
    def accept(self, visitor: Visitor) -> object:
        return visitor.visit_binary_expr(self)
class Unary(object):
    def __init__(self, operator: Token, right: Expr) -> None:
        self.operator: Token = operator
        self.right: Expr = right
    def accept(self, visitor: Visitor) -> object:
        return visitor.visit_unary_expr(self)
class Grouping(object):
    def __init__(self, expression: Expr) -> None:
        self.expression: Expr = expression
    def accept(self, visitor: Visitor) -> object:
        return visitor.visit_grouping_expr(self)
class Literal(object):
    def __init__(self, value: object) -> None:
        self.value: object = value
    def accept(self, visitor: Visitor) -> object:
        return visitor.visit_literal_expr(self)
