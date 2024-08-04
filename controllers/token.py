
from datetime import datetime, timedelta
from fastapi import HTTPException, Depends,status
from sqlalchemy import select
from sqlalchemy.orm import Session

from model.core import User
from secure import oauth2_schema
from typing import Optional
from model.database import SessionLocal, engine
import jwt

SECRET_KEY = '52367badbf4e42f3a94d9ce456e1f01cbfee36a604da5c9589fa84f0bb9e661b'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(oauth2: str = Depends(oauth2_schema), db: Session = Depends(get_db)):
    credentials_exeption = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authneticate': 'Bearer'}
    )

    try:
        payload = jwt.decode(oauth2, SECRET_KEY, algorithms=[ALGORITHM])
        decode_username: str = payload.get('username')

        if decode_username is None:
            raise credentials_exeption
    except HTTPException:
        raise credentials_exeption

    user: User = db.scalar(select(User).where(User.email == decode_username))

    if user is None:
        raise credentials_exeption

    return user


