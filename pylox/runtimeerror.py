from pylox.token import Token

class PyloxRuntimeError(Exception):
    def __init__(self, token: Token, message: str) -> None:
        super().__init__(message)
        self.message = message
        self.token = token
