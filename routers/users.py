

from fastapi import Depends, HTTPException, APIRouter, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession as Session
from controllers import token
from controllers.token import get_current_user
from controllers.users import register
from model import crud, schemas
from model.core import User, Item
from model.database import SessionLocal
from secure import pwd_context


router = APIRouter()


# Dependency
async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()


@router.get("/{item_id}")
async def read_item(item_id: int, db: Session = Depends(get_db)):
    item: Item = await db.scalar(select(Item).where(Item.id == item_id))
    if not item:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="item not found")
    item.view = item.view + 1
    await db.commit()
    await db.refresh(item)
    return item



@router.get("/popular/")   
async def most_popular_items(amount: int, db: Session = Depends(get_db)):   
    popular = await db.execute(select(Item).order_by((Item.view.desc()),(Item.id.desc())).limit(amount))
    return popular.scalars().all()


@router.get("/new/")   
async def new_items(amount: int, db: Session = Depends(get_db)):   
    new = await db.execute(select(Item).order_by((Item.id.desc())).limit(amount))
    return new.scalars().all()


@router.get("/old/")   
async def old_items(amount: int, db: Session = Depends(get_db)):   
    old = await db.execute(select(Item).order_by((Item.id)).limit(amount))
    return old.scalars().all()


@router.get("/dont-popular/")   
async def dont_popular_items(amount: int, db: Session = Depends(get_db)):   
    dont_popular = await db.execute(select(Item).order_by((Item.view)).limit(amount))
    return dont_popular.scalars().all()


@router.post("/users/register", response_model=schemas.UserCreate, status_code=201)
async def register_user(user_data: schemas.UserCreate, db: Session = Depends(get_db)):
    return await register(db=db, user_data=user_data)


@router.post('/token/', status_code=201)
async def get_token(request: OAuth2PasswordRequestForm = Depends(),
                    db: Session = Depends(get_db)):
    user: User = await db.scalar(select(User).where(User.email == request.username))
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
    try:
        return current_user
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Login please')


@router.put("/user-is0")
async def close_user(db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(get_current_user)):
    try:
        if current_user.is_active == 1:
            user: User = await db.scalar(select(User).where(User.email == current_user.email))
            user.is_active = 0
            await db.commit()
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='You account is busy')

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f'{e}')


@router.put("/user-is1")
async def open_user(db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(get_current_user)):
    try:
        if current_user.is_active == 0:
            user: User = await db.scalar(select(User).where(User.email == current_user.email))
            user.is_active = 1
            await db.commit()
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='You account is not busy')

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f'{e}')


@router.delete("/delete-you-user")
async def delete_you_user(current_user: schemas.UserBase = Depends(get_current_user),db: Session = Depends(get_db)):
    delete: User = await db.scalar(select(User).where(User.email == current_user.email))
    if not delete:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found")
    await db.delete(delete)
    await db.commit()
    return {
        'deleted you user': current_user.email
    }
    # The front end should remove the client's jwt from memory or another location


@router.post("/create-item")
async def create_item(itemuserdata: schemas.ItemBase, db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(get_current_user)):
    await db.scalar(select(Item))
    item = Item(owner_id=current_user.id)
    item.title = itemuserdata.title
    item.description = itemuserdata.description
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return {
        'created item from id user': current_user.id,
        'item id': item.id,
    }


@router.delete("/delete-item")
async def delete_item(userdata: schemas.ItemDel, current_user: schemas.UserBase = Depends(get_current_user), db: Session = Depends(get_db)):
 try:
    valid: Item = await db.scalar(select(Item).where(Item.id == userdata.id))
    if valid.owner_id == current_user.id:
        await db.delete(valid)
        await db.commit()
        return {
        'deleted you item': userdata.id
        }
 except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You cannot delete an item that is not yours")

