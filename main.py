from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import testRouter
from .routers import user as user_router
from .depends import create_db_and_tables
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(), override=True)
#可以像访问系统环境变量一样使用 .env 文件中的变量，例如 os.getenv(key, default=None)


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

app.include_router(testRouter.router)
app.include_router(user_router.router)

@app.get("/")
async def read_root():
    return {"Hello": "World"}

