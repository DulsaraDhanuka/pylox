class Logger():
    has_error = False
    def __init__(self) -> None: pass

    def report(line: int, where: str, message: str) -> None:
        print(f"[line {line}] Error{where}: {message}")

    def error(line: int, message: str) -> None:
        Logger.report(line, "", message)
        Logger.has_error = True

