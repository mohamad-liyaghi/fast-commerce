class AdminRequiredException(Exception):
    def __init__(self, message="Admin required"):
        self.message = message
        super().__init__(self.message)
