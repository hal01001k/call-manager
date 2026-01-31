import os
from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import status 

security = HTTPBearer()

TOKEN = os.environ.get("AUTH_TOKEN", "super-secret-token-123")

def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)) -> str:
    if credentials.credentials != TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return credentials.credentials
