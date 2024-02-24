from abc import ABC, abstractmethod

class Visitor(ABC):
    @abstractmethod
    def visit_unary_expr(self, expr: Unary) -> object:
        pass
    @abstractmethod
    def visitBinaryExpr(self, expr: Binary) -> object:
        pass
    @abstractmethod
    def visitGroupingExpr(self, expr: Grouping) -> object:
        pass
    @abstractmethod
    def visitLiteraleExpr(self, expr: Literal) -> object:
        pass

class Expr(ABC):
    @abstractmethod
    def accept(visitor: Visitor) -> object:
        pass
class Binary(Expr):
    def __init__(self, left: Expr, operator: Token, right: Expr) -> None:
        self.left: Expr = left
        self.operator: Token = operator
        self.right: Expr = right
    def accept(visitor: Visitor) -> object:
        return visitor.visitBinaryExpr(self)
class Unary(Expr):
    def __init__(self, operator: Token, right: Expr) -> None:
        self.operator: Token = operator
        self.right: Expr = right
    def accept(visitor: Visitor) -> object:
        return visitor.visitUnaryExpr(self)
class Grouping(Expr):
    def __init__(self, expression: Expr) -> None:
        self.expression: Expr = expression
    def accept(visitor: Visitor) -> object:
        return visitor.visitGroupingExpr(self)
class Literal(Expr):
    def __init__(self, value: object) -> None:
        self.value: object = value
    def accept(visitor: Visitor) -> object:
        return visitor.visitLiteralExpr(self)

