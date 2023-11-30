from typing import Callable

from fastapi import Depends
from fastapi.security import HTTPBasicCredentials, HTTPBasic

from uberserver_src.errors.authentication_errors import BadCredentials, ForbiddenUser

basic_auth = HTTPBasic()

AUTHENTICATED_USERS_KEYS = {
    546: "2157hiuohj===GTDSf",
    897: "asdhfdjkDGDSGsg4df",
    231: "BNVBHU==57654ghdgf",
}


def require_authentication() -> Callable[[HTTPBasicCredentials], None]:
    def authenticate_key(credentials: HTTPBasicCredentials = Depends(basic_auth)):
        if user_key := AUTHENTICATED_USERS_KEYS.get(int(credentials.username)):
            if user_key == credentials.password:
                return
            raise BadCredentials()
        raise ForbiddenUser()

    return authenticate_key
