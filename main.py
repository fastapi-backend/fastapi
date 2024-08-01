from fastapi import FastAPI
from model import core
from model.database import engine
from routers.items import router as items_router
from routers.items import router as users_router

core.Base.metadata.create_all(bind=engine)
app = FastAPI()


app.include_router(
    router=items_router,
    prefix='/items',
)


app.include_router(
    router=items_router,
    prefix='/users',
)
