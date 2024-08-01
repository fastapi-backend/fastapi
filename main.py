from fastapi import FastAPI
from routers.items import router as items_router
app = FastAPI()


app.include_router(
    router=items_router,
    prefix='/items',
)
