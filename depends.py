import logging
from os import getenv

from sqlmodel import create_engine
from fastapi_mail import FastMail,ConnectionConfig
from pydantic import EmailStr,TypeAdapter,SecretStr
from .dependencies.datamodel import *

use_sqlite = getenv("USE_SQLITE",default="yes")
use_mysql = getenv("USE_MYSQL",default="no")

# 邮件配置
email_str = TypeAdapter(EmailStr)
email_key = TypeAdapter(SecretStr)
mail_username = getenv("MAIL_USERNAME", "test")
mail_password = getenv("MAIL_PASSWORD", email_key.validate_python("test"))
mail_from = getenv("MAIL_FROM", email_str.validate_python("example@example.com"))
mail_port = getenv("MAIL_PORT", 587)
mail_server = getenv("MAIL_SERVER", "example.com")
mail_starttls = getenv("MAIL_STARTTLS", True)
mail_ssl_tls = getenv("MAIL_SSL_TLS", False)
mail_use_credentials = getenv("MAIL_USE_CREDENTIALS", True)
email_template_folder = getenv("EMAIL_TEMPLATE_FOLDER", "./email_templates")

if use_sqlite == "yes":
    sqlite_uri = getenv("SQLALCHEMY_DATABASE_URI",default="sqlite:///sqlite0.db")
    connect_args = {"check_same_thread": False}
    engine = create_engine(sqlite_uri, connect_args=connect_args)

elif use_mysql == "yes":
    mysql_user = getenv("MYSQL_USER", "root")
    mysql_password = getenv("MYSQL_PASSWORD", "default")
    mysql_host = getenv("MYSQL_HOST", "localhost")
    mysql_port = getenv("MYSQL_PORT", "3306")
    mysql_database = getenv("MYSQL_DATABASE", "FastAuthService")
    mysql_uri = f"mysql+pymysql://{mysql_user}:{mysql_password}@{mysql_host}:{mysql_port}/{mysql_database}"
    connect_args = {"charset": "utf8mb4","connect_timeout": 10}
    engine = create_engine(
        mysql_uri,
        connect_args=connect_args,
        pool_pre_ping=True,
        pool_recycle=3600,
        echo=True,  # 输出 SQL 日志（调试用）
        pool_size=10,  # 连接池大小
        max_overflow=15,  # 最大溢出连接数
    )
else:
    raise ValueError("Unsupported SQLAlchemy engine type")

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
mail = FastMail(email_config)

verification_codes = {}

verification_emails = {}
# 待验证邮件信息, 目前未启用


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def drop_db_and_tables():
    # danger!!!!
    SQLModel.metadata.drop_all(engine)

def get_logger(name) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    return logger

