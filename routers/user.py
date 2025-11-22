from fastapi import APIRouter
from ..dependencies import requestModel
# from ..crud.dbDependencies import SessionDep
router = APIRouter()

@router.post("/api/user/login")
async def user_login(data:requestModel.UserLogin):
    user_email = data.email
    return {"user_email":user_email}

