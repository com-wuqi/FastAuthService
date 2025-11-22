from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import user as user_router
from .dataBase import create_db_and_tables

create_db_and_tables()

app = FastAPI(debug=True)

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(user_router.router)

@app.get("/")
async def read_root():
    return {"Hello": "World"}

