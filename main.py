from fastapi import FastAPI
from routers.items import router as items_router
from routers.users import router as users_router
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(
 router=items_router,
 prefix='/items',)


app.include_router(
    router=users_router,
    prefix='/test',
)
