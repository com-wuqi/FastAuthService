from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv(), override=True)

import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import testRouter
from .routers import user as user_router
from .routers import funcRouter as func_router
from .routers import mailRouter as mail_router
from .depends import *
from contextlib import asynccontextmanager
from .background_checker import UserDataChecker
from fastapi_mail import FastMail,ConnectionConfig

background_checker = None
logger = get_logger(__name__)

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

email_config = ConnectionConfig(
    MAIL_USERNAME=mail_username,
    MAIL_PASSWORD=mail_password,
    MAIL_FROM=mail_from,
    MAIL_PORT=mail_port,
    MAIL_SERVER=mail_server,
    MAIL_STARTTLS=mail_starttls,
    MAIL_SSL_TLS=mail_ssl_tls,
    USE_CREDENTIALS=mail_use_credentials,
    TEMPLATE_FOLDER=email_template_folder
)

app = FastAPI(debug=True,lifespan=lifespan)
mail = FastMail(email_config)

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
app.include_router(mail_router.router)

@app.get("/")
async def read_root():
    return {"Hello": "World"}

