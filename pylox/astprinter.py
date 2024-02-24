from pylox.expr import Visitor, Expr, Binary, Unary, Grouping, Literal

class AstPrinter(Visitor):
    def print(self, expr: Expr) -> str:
        return expr.accept(self)

    def visit_binary_expr(self, expr: Binary) -> object:
        return f"({expr.operator.lexeme} {expr.left.accept(self)} {expr.right.accept(self)})"

    def visit_unary_expr(self, expr: Unary) -> object:
        return f"({expr.operator.lexeme} {expr.right.accept(self)})"

    def visit_grouping_expr(self, expr: Grouping) -> object:
        return f"(group {expr.expression.accept(self)})"

    def visit_literal_expr(self, expr: Literal) -> object:
        if expr.value is None: return "nil"
        return f"{str(expr.value)}"

