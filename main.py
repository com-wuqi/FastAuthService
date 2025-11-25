from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv(), override=True)

import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import testRouter
from .routers import user as user_router
from .routers import funcRouter as func_router
from .depends import create_db_and_tables
from contextlib import asynccontextmanager
from .background_checker import UserDataChecker

#可以像访问系统环境变量一样使用 .env 文件中的变量，例如 os.getenv(key, default=None)


background_checker = None

@asynccontextmanager
async def lifespan(_: FastAPI):
    create_db_and_tables()

    checker = UserDataChecker()
    global background_checker
    background_checker = checker
    task = asyncio.create_task(checker.start_checking())

    yield

    if background_checker:
        background_checker.stop_checking()
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass

app = FastAPI(debug=True,lifespan=lifespan)

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

app.include_router(testRouter.router)
app.include_router(user_router.router)
app.include_router(func_router.router)

@app.get("/")
async def read_root():
    return {"Hello": "World"}

