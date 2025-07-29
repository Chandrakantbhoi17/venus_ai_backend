from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.base import get_db
from app.core.config import settings
from .exceptions import InvalidOrExpiredTokenException,UserNotFoundException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .security import decode_token
security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials  # This extracts just the token part
    payload = decode_token(token)

    if not payload or "sub" not in payload:
        raise InvalidOrExpiredTokenException()

   
    user = db.query(User).filter(User.email ==payload['sub']).first()

    if not user:
        raise UserNotFoundException()

    return user

