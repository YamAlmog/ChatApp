
class messageManagerException(Exception):
    def __init__(self, message):
        super().__init__(message)


class InvalidUserName(Exception):
    def __init__(self, message):
        super().__init__(message)

class InvalidPassword(Exception):
    def __init__(self, message):
        super().__init__(message)
