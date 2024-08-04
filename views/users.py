from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from controllers.token import get_current_user



async def get_blog(id: int = None, db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(get_current_user)):
    blog = db_queries.get_blog(db, id)
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='There is no blog post in db')
    # return blog
    return {
        'data': blog,
        'current_user': current_user
    }


