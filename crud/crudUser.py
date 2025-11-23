from .dbDependencies import SessionDep
from ..dependencies.datamodel import *
from ..depends import get_logger
import sqlalchemy.exc
logger = get_logger(__name__)
"""
数据库操作
"""
def create_user(users:User,session: SessionDep) -> int:
    states = 0
    session.add(users)
    try:
        session.commit()
        logger.info(f"created user: {users.email}")
        session.refresh(users)
    except sqlalchemy.exc.IntegrityError:
        states = 1
        session.rollback()
        logger.warning(f"email already exists: {users.email}")


    return states
