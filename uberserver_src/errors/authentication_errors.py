class AuthenticationError(Exception):
    pass


class BadCredentials(AuthenticationError):
    pass


class ForbiddenUser(AuthenticationError):
    pass
