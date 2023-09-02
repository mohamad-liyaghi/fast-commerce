from .core import AlreadyExistError, NotFoundError


class UserAlreadyExistError(AlreadyExistError):
    def __init__(self, message: str = "User already exist") -> None:
        self.message = message
        super().__init__(self.message)


class UserPendingVerificationError(Exception):
    def __init__(self, message: str = "User is pending verification") -> None:
        self.message = message
        super().__init__(self.message)


class UserNotFoundError(NotFoundError):
    def __init__(self, message: str = "User not found") -> None:
        self.message = message
        super().__init__(self.message)


class InvalidVerificationCodeError(Exception):
    def __init__(self, message: str = "Invalid verification code") -> None:
        self.message = message
        super().__init__(self.message)


class InvalidCredentialsError(Exception):
    def __init__(self, message: str = "Invalid credentials") -> None:
        self.message = message
        super().__init__(self.message)
