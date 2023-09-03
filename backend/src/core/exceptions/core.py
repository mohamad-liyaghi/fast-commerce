class AlreadyExistError(Exception):
    def __init__(self, message: str = "Already exist") -> None:
        self.message = message
        super().__init__(self.message)


class NotFoundError(Exception):
    def __init__(self, message: str = "Not found") -> None:
        self.message = message
        super().__init__(self.message)
