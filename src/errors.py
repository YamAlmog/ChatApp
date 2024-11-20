
class MessageManagerException(Exception):
    def __init__(self, message):
        super().__init__(message)

class UsersManagerException(Exception):
    def __init__(self,message):
        super().__init__(message)


class InvalidUserName(Exception):
    def __init__(self, message):
        super().__init__(message)

class InvalidPassword(Exception):
    def __init__(self, message):
        super().__init__(message)


class InvalidToken(Exception):
    def __init__(self, message):
        super().__init__(message)


class UnregisteredUser(Exception):
    def __init__(self, message):
        super().__init__(message)
