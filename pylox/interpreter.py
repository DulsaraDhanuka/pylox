from pylox.token import Token
from pylox.expr import Visitor, Expr, Binary, Unary, Grouping, Literal
from pylox.tokentypes import TokenType
from pylox.logger import Logger
from pylox.runtimeerror import PyloxRuntimeError

class Interpreter(Visitor):
    def interpret(self, expr: Expr) -> None:
        try:
            value = self.evaluate(expr)
            print(self.stringify(value))
        except PyloxRuntimeError as e:
            Logger.runtime_error(e)

    def stringify(self, value: object) -> str:
        if value is None: return "nil"

        if isinstance(value, float): return f"[number {value}]"
        if isinstance(value, bool): 
            if value:
                return f"[bool true]"
            else:
                return f"[bool false]"
        if isinstance(value, str): return f'[string "{str(value)}"]'

    def evaluate(self, expr: Expr) -> object:
        return expr.accept(self)

    def visit_binary_expr(self, expr: Binary) -> str:
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

        if expr.operator.tokentype == TokenType.MINUS:
            self._check_number_operand(expr.operator, left, right)
            return float(left) - float(right)
        elif expr.operator.tokentype == TokenType.STAR:
            self._check_number_operand(expr.operator, left, right)
            return float(left) * float(right)
        elif expr.operator.tokentype == TokenType.SLASH:
            self._check_number_operand(expr.operator, left, right)
            return float(left) / float(right)
        elif expr.operator.tokentype == TokenType.PLUS:
            if isinstance(left, float) and isinstance(right, float):
                return float(left) + float(right)
            elif isinstance(left, str) and isinstance(right, str):
                return str(left) + str(right)
            else:
                raise PyloxRuntimeError(expr.operator, "Operands must be two numbers or two strings.")
        elif expr.operator.tokentype == TokenType.GREATER:
            self._check_number_operand(expr.operator, left, right)
            return float(left) > float(right)
        elif expr.operator.tokentype == TokenType.GREATER_EQUAL:
            self._check_number_operand(expr.operator, left, right)
            return float(left) >= float(right)
        elif expr.operator.tokentype == TokenType.LESS:
            self._check_number_operand(expr.operator, left, right)
            return float(left) < float(right)
        elif expr.operator.tokentype == TokenType.LESS_EQUAL:
            self._check_number_operand(expr.operator, left, right)
            return float(left) <= float(right)
        elif expr.operator.tokentype == TokenType.EQUAL_EQUAL:
            return self._is_equal(left, right)
        elif expr.operator.tokentype == TokenType.BANG_EQUAL:
            return not self._is_equal(left, right)
        # This is unreachable
        return None

    def _is_equal(self, val1, val2) -> bool:
        return isinstance(val1, type(val2)) and isinstance(val2, type(val1)) and val1 == val2

    def visit_unary_expr(self, expr: Unary) -> str:
        right = self.evaluate(expr.right)
        if expr.operator.tokentype == TokenType.MINUS:
            self._check_number_operand(expr.operator, right)
            return -float(right)
        elif expr.operator.tokentype == TokenType.BANG:
            return not self._is_truthy(right)
        # This is unreachable
        return None
    
    def _check_number_operand(self, operator: Token, *operands) -> None:
        if sum([not isinstance(operand, float) for operand in operands]) == 0: return
        raise PyloxRuntimeError(operator, "Operand must be a number.")

    def _is_truthy(self, obj: object):
        if obj is None: return False
        if isinstance(obj, bool): return obj
        if isinstance(obj, float) and obj == 1.0: return True
        if isinstance(obj, float) and obj == 0.0: return False
        return True

    def visit_grouping_expr(self, expr: Grouping) -> object:
        return evaluate(expr)

    def visit_literal_expr(self, expr: Literal) -> object:
        return expr.value

