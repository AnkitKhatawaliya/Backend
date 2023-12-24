import jwt
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

SECRET_KEY = "w2ws3def3w4r5t"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def create_jwt_token(UserName: str, user_role: str):
    expiration_time = datetime.utcnow() + timedelta(days=60)
    payload = {"sub": UserName, "exp": expiration_time, "role": user_role}
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials; some error occurred",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_name = payload.get("sub")
        role = payload.get("role")
        if user_name is None:
            raise credentials_exception
        return user_name, role
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_426_UPGRADE_REQUIRED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise credentials_exception


def create_jwt_token_int(user_id: int,  user_role: str):
    expiration_time = datetime.utcnow() + timedelta(days=60)
    payload = {"sub": user_id, "exp": expiration_time, "role": user_role}
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token


def get_current_user_int(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials; some error occurred",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("sub")
        role = payload.get("role")
        if user_id is None:
            raise credentials_exception
        return user_id , role
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_426_UPGRADE_REQUIRED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise credentials_exception
