from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt
import time

from app.infra.depends import SSDLCContainer


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)
        self.jwt_secret_key = SSDLCContainer.config()['auth']['jwt_secret_key']
        self.jwt_algorithm =  SSDLCContainer.config()['auth']['jwt_algorithm']

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, token: str) -> bool:
        is_token_valid: bool = False

        try:
            payload = jwt.decode(token, self.jwt_secret_key, algorithms=[self.jwt_algorithm])
            payload = None if payload["exp"] <= time.time() else payload
        except Exception: #TODO: Бредовая обработка исключений
            payload = None

        if payload:
            is_token_valid = True

        return is_token_valid
