from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session


from model.core import User


def get_user_by_token(db: Session):
    user: User = db.scalar(select(User))
    if user:
        return user


