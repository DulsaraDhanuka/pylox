from pylox.tokentypes import TokenType

class Logger():
    has_error = False
    def __init__(self) -> None: pass

    def report(line: int, where: str, message: str) -> None:
        print(f"[line {line}] Error{where}: {message}")

    def error(message: str, line: int = None, token = None) -> None:
        if line is not None:
            Logger.report(line, "", message)
            Logger.has_error = True
        if token is not None:
            if token.tokentype == TokenType.EOF:
                Logger.report(line, " at end", message)
            else:
                Logger.report(line, f"at '{token.lexeme}'", message)
    

