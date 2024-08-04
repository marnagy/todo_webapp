from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwt import decode as jwt_decode

from crud import ALGORITHM, SECRET_KEY


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            print(credentials)
            if not credentials.scheme == "Bearer":
                print("Scheme:", credentials.scheme)
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials):
                print("Credentials:", credentials.credentials)
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, jwtoken: str) -> bool:
        isTokenValid: bool = False
        print("JWtoken:", jwtoken)

        #try:
        payload = jwt_decode(jwtoken, SECRET_KEY, algorithms=[ALGORITHM])
        # except:
        #     payload = None
        print("Payload:", payload)
        if payload:
            isTokenValid = True

        return isTokenValid