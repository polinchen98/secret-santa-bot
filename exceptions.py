class UserAlreadyExistsError(Exception):
    message = "User with such id is already recorded"


class UserNotExistsError(Exception):
    message = "User with such id was not found"


class ThereAreNotAvailableUsers(Exception):
    message = "There are not available users now"
