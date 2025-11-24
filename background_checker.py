import asyncio
from datetime import timedelta

from sqlmodel import select

from .crud.dbDependencies import *
from .dependencies.datamodel import *
from .depends import get_logger

logger = get_logger(__name__)

class UserDataChecker:
    def __init__(self):
        # self.db = db
        self.is_running = False

    async def start_checking(self):
        """启动后台检查任务"""
        self.is_running = True
        logger.info("checker started")

        while self.is_running:
            try:
                await self.check_and_update_users()
                # 每60秒检查一次
                await asyncio.sleep(60)
            except Exception as e:
                logger.error(f"checker failed: {e}")
                await asyncio.sleep(30)  # 出错时等待时间短一些

    @staticmethod
    async def check_and_update_users():
        # 检查并重置长时间未活动的用户
        # 为了方便，管理员用户不会被登出
        db = get_session_for_background()
        try:
            cutoff_time = datetime.now(timezone.utc) - timedelta(days=30)
            inactive_users = db.exec(select(User).where(
            User.last_login < cutoff_time,
            User.is_active == True)).all()
            for user in inactive_users:
            # 修补为不活跃，登出
                logger.warning("fixing users' status...")
                user.is_active = False
            db.commit()
        except Exception as e:
            logger.error(e)
            db.rollback()
        finally:
            db.close()

    def stop_checking(self):
        """停止检查服务"""
        self.is_running = False
        logger.info("checker stopped")
