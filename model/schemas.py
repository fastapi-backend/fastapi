from pydantic import BaseModel, EmailStr


class ItemBase(BaseModel):
    title: str
    description: str | None = None


class ItemCreate(ItemBase):
    pass


class ItemDel(BaseModel):
    id: int

    class Config:
        orm_mode = True


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str

    class Config:
        orm_mode = True


class LiteUser(UserBase):
    id: int

    class Config:
        orm_mode = True


class Connect(BaseModel):
    auth: str

    class Config:
        orm_mode = True


class User(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True