class UberServerError(Exception):
    pass


class UberServerTimeOut(UberServerError):
    pass


class UberServerUnexpectedStatus(UberServerError):
    pass


class UberServerVIPNotFound(UberServerError):
    pass
