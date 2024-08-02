from sqlalchemy.orm import Session


from model import core


def get_users(db: Session, skip: int = 0):
    return db.query(core.User).offest(skip).all()
