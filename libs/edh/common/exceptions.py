class EDHTaskError(BaseException):
    def __init__(self, task: str, message: str):
        self.task = task
        self.message = message
        super().__init__(message)
