import uuid

from datetime import datetime, timedelta
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette.status import HTTP_404_NOT_FOUND
from model.core import User, Token
from model.schemas import UserCreate
from secure import pwd_context
from typing import Optional
import jwt

SECRET_KEY = '52367badbf4e42f3a94d9ce456e1f01cbfee36a604da5c9589fa84f0bb9e661b'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def login(db: Session, user_data: UserCreate):
    user: User = db.scalar(select(User).where(User.email == user_data.email))
    if not user:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    if not pwd_context.verify(user_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    token: Token = Token(user_id=user.id, access_token=str(uuid.uuid4()))
    db.add(token)
    db.commit()
    return{"access_token": token.access_token}
