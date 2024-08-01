from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session


from controllers.users import get_users
from model.database import get_db


router = APIRouter()


@router.get("/",)
def read_users(skip: int = 0, db: Session = Depends(get_db)):
    users = get_users(db,skip=skip)
    return users
