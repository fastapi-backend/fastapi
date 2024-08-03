

from fastapi import Depends, FastAPI, HTTPException, APIRouter
from sqlalchemy.orm import Session

from controllers.token import login
from controllers.users import register
from model import crud, core, schemas
from model.database import SessionLocal, engine
from secure import apikey_scheme
from typing import Annotated

from views.users import get_user_by_token

core.Base.metadata.create_all(bind=engine)
router = APIRouter()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@router.post("/users/register", response_model=schemas.User, status_code=201)
def register_user(user_data: schemas.UserCreate, db: Session = Depends(get_db)):
    return register(db=db, user_data=user_data)


@router.post("/users/login", response_model=schemas.Token, status_code=201)
def login_user(user_data: schemas.UserCreate, db: Session = Depends(get_db)):
    return login(db=db, user_data=user_data)


@router.get("/profile/", response_model=schemas.User)
def login_profile(access_token: Annotated[str, Depends(apikey_scheme)], db: Session = Depends(get_db)):
    return get_user_by_token(access_token=access_token, db=db)
        
