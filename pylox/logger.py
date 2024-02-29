from pylox.tokentypes import TokenType
from pylox.runtimeerror import PyloxRuntimeError

class Logger():
    has_error = False
    has_runtime_error = False
    def __init__(self) -> None: pass

    def report(line: int, where: str, message: str) -> None:
        print(f"[line {line}] Error{where}: {message}")

    def error(message: str, line: int = None, token = None) -> None:
        Logger.has_error = True
        if line is not None:
            Logger.report(line, "", message)
        if token is not None:
            if token.tokentype == TokenType.EOF:
                Logger.report(line, " at end", message)
            else:
                Logger.report(line, f" at '{token.lexeme}'", message)
    
    def runtime_error(e: PyloxRuntimeError) -> None:
        Logger.has_runtime_error = True
        print(f"[line {e.token.line}] RuntimeError: {e.message}")

