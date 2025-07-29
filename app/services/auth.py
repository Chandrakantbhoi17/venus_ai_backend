
from fastapi import Depends,Header
from app.models.user import User
from app.models.base import get_db
from fastapi import HTTPException,status
from app.services import user as  user_service
from sqlalchemy.orm import Session
from app.core import exceptions
from app.core import auth,security as security_util
from app.core.config import settings
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()


from app.core import auth  as auth_util 
def authenticate_user(form_data,db: Session):
    # """Authenticate user by email and password, return JWT if valid."""
    # # Retrieve user from the database by email
    db_user = user_service.get_user_by_email(db,form_data.email)
   
    if  db_user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
    
 
        

    if not security_util.verify_password(form_data.password, db_user.password):
        
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
    # Prepare user data for JWT creation (e.g., user ID or email)
    user_data = {"sub": str(db_user.id),"email":str(db_user.email),'role':str(db_user.role.value)}  # 'sub' is commonly the user ID or email
        
    # Generate JWT token
    access_token = auth_util.create_access_token(data=user_data)
    refresh_token=auth_util.create_refresh_token(data=user_data)

        
    # Return the access token in the response
    return {"access_token": access_token,"refresh_token": refresh_token, "token_type": "bearer"}


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials  # This extracts just the token part
    payload = auth_util.decode_access_token(token)

    if not payload or "sub" not in payload:
        raise exceptions.InvalidOrExpiredTokenException()

    user_id = payload["sub"]
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise exceptions.UserNotFoundException()

    return user


def get_access_token_by_refresh_token(refresh_token: str, db : Session = Depends(get_db)):
    """Validates the refresh token and returns a new access token."""
   
    # payload=auth.decode_refresh_token(refresh_token.refresh_token)
 

    # user_id = payload.get("sub")
    # email = payload.get("email")
    # if not user_id or not email:
    #    raise exceptions.InvalidRefreshTokenException()
    #     # Verify if the user exists in the database
    user = db.query(User).filter(User.email == "user@example@gmail.com").first()
    
    # if not user:
    #         raise exceptions.UserNotFoundException()

    # new_access_token = auth.create_access_token({"sub": str(user.id), "email": user.email})

    return {"access_token":"new_access_token", "token_type": "bearer"}
