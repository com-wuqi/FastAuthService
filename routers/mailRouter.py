from fastapi import APIRouter
from ..dependencies.emailHelper import *
from ..dependencies import requestModel
import asyncio

logger = get_logger(__name__)
router = APIRouter()

verification_codes = {}
# TODO: 完善销毁超时code的功能

# TODO: 完善并且测试接口
@router.post("/api/email/send_email")
async def send_email(data: requestModel.EmailRequest):
    # 基础邮件发送
    pass

@router.post("/api/email/send_verification_code")
async def send_verification_code(data: requestModel.VerifyEmailRequest):
    # 发送邮件验证码
    pass

@router.post("/api/email/verify_code")
async def verify_code(data: requestModel.VerifyEmailRequest):
    # 校验邮件验证码
    pass

@router.post("/api/user/reset_password")
async def reset_user_password(data: requestModel.ResetPassword):
    # 重置用户密码
    pass

@router.post("/api/user/verifyEmail")
async def verify_user_email(data: requestModel.VerifyEmailRequest):
    # 发送验证用户邮件的邮件(注册时)
    pass

@router.post("/api/user/sendVerificationEmail")
async def send_verification_email(data: requestModel.ResetPassword):
    # 验证邮件(注册时)
    pass