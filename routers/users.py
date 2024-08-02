from fastapi import Depends, FastAPI, HTTPException, APIRouter
from sqlalchemy.orm import Session

from controllers.users import register
from model import crud, core, schemas
from model.database import SessionLocal, engine
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


@router.post("/users/register",response_model=schemas.User,status_code=201)
def register_user(user_data: schemas.UserCreate, db: Session = Depends(get_db)):
    return register(db=db, user_data=user_data)
