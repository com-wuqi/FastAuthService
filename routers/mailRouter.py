from fastapi import APIRouter,HTTPException

from ..dependencies.secureHelper import generate_email_verification_code
from ..dependencies.emailHelper import *
from ..dependencies import requestModel,secureHelper
from ..depends import verification_codes,verification_emails
import asyncio

logger = get_logger(__name__)
router = APIRouter()

@router.post("/api/email/send_email")
async def send_email(data: requestModel.EmailRequest):
    # 基础邮件发送
    result = await EmailService.send_common_email(subject=data.subject,recipients=data.recipients,body=data.body)
    if result:
        logger.info(f"""subject: {data.subject},recipients: {data.recipients},body: {data.body} successfully sent to {data.recipients}""")
        return {"status":True}
    else:
        logger.warning(f"""subject: {data.subject},recipients: {data.recipients},body: {data.body} failed to send to {data.recipients}""")
        return {"status":False}

@router.post("/api/email/send_verification_code")
async def send_verification_code(data: requestModel.ResetPassword):
    # 发送邮件验证码
    # 内部接口, 没有校验用户权限
    code = generate_email_verification_code()
    if data.recipient in verification_codes:
        if verification_codes[data.recipient]["resend_limit"] > asyncio.get_event_loop().time():
            # 当前不可重新发送验证码, 间隔过短
            logger.warning(f"email : {data.recipient} resend limit reached")
            raise HTTPException(status_code=403, detail="Resend limit exceeded")
    verification_codes[data.recipient]={
        "code":code,
        "resend_limit":asyncio.get_event_loop().time()+120,
        "expires":asyncio.get_event_loop().time()+300
    }
    result = await EmailService.send_verify_email(email=data.recipient,code=code)
    if result:
        return {"status":True}
    else:
        logger.warning(f"email send_verification_code failed to send to {data.recipient}")
        return {"status":False}

@router.post("/api/email/verify_code")
async def verify_code(data: requestModel.VerifyEmailRequest):
    # 校验邮件验证码
    # 内部接口, 没有校验用户权限
    if data.recipient in verification_codes:
        if verification_codes[data.recipient]["expires"] > asyncio.get_event_loop().time():
            if verification_codes[data.recipient]["code"] == data.code:
                del verification_codes[data.recipient]
                return {"status":True}
            else:
                logger.warning(f"failed to verify code for {data.recipient} : Wrong code")
                raise HTTPException(status_code=404)
        else:
            # 超时
            del verification_codes[data.recipient]
            logger.warning(f"failed to verify code for {data.recipient} : Timeout")
            raise HTTPException(status_code=404)
    else:
        # 不存在
        logger.warning(f"failed to verify code for {data.recipient} : Not found")
        raise HTTPException(status_code=404)


@router.post("/api/user/reset_password")
async def reset_user_password(data: requestModel.ResetPassword):
    # 重置用户密码, 需要鉴权
    # TODO: 完善并且测试接口
    pass

# 使用 code 完成
# @router.post("/api/user/verifyEmail")
# async def verify_user_email(data: requestModel.ResetPassword):
#     # 发送验证用户邮件的邮件(注册时)
#     pass
#
# @router.post("/api/user/sendVerificationEmail")
# async def send_verification_email(data: requestModel.VerifyEmailRequest):
#     # 验证邮件(注册时)
#     pass