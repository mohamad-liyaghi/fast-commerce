from fastapi import Depends, status, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer


class AuthenticationRequired:
    """
    Make sure the user is authenticated.
    """
    def __init__(
        self,
        token: HTTPAuthorizationCredentials = Depends(HTTPBearer(auto_error=False)),
    ):
        if not token:
            raise HTTPException(
                detail="Authentication required",
                status_code=status.HTTP_403_FORBIDDEN
            )
