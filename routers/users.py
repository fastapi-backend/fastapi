

from fastapi import Depends, HTTPException, APIRouter, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from controllers import token
from controllers.token import get_current_user
from controllers.users import register
from model import crud, schemas
from model.core import User
from model.database import SessionLocal
from secure import pwd_context


router = APIRouter()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip)
    return users


@router.post("/users/register", response_model=schemas.User, status_code=201)
def register_user(user_data: schemas.UserCreate, db: Session = Depends(get_db)):
    return register(db=db, user_data=user_data)


@router.post('/token/', status_code=201)
async def get_token(request: OAuth2PasswordRequestForm = Depends(),
                    db: Session = Depends(get_db)):
    user: User = db.scalar(select(User).where(User.email == request.username))
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Invalid credentials')
    if not pwd_context.verify(request.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Invalid username or password')

    access_token = token.create_access_token(data={'username': user.email})

    return {
        'access_token': access_token,
        'token_type': 'bearer',
        'username': user.email,
    }


@router.get("/profile/", response_model=schemas.User)
async def get_user(db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(get_current_user)):
    return current_user

        
