from fastapi import APIRouter,HTTPException
from ..dependencies import requestModel,secureHelper
from ..dependencies.datamodel import *
from ..crud.dbDependencies import SessionDep
from ..crud import crudUser
router = APIRouter()

@router.post("/api/user/login")
async def user_login(data:requestModel.UserLogin):
    user_email = data.email
    return {"user_email":user_email}

@router.post("/api/user/logout")
async def user_logout(data:requestModel.UserLogout):
    pass

@router.post("/api/user/register")
async def user_register(data:requestModel.UserRegister,session: SessionDep):
    user_password = data.password
    user_name = data.name
    user_email = data.email
    user_password_salt = secureHelper.generate_salt()
    user_secret_key = secureHelper.generate_secret_key()
    hashed_password = secureHelper.hash_salted_password(user_password, user_password_salt)
    user = User(
        name=user_name,
        email=user_email,
        password=hashed_password,
        password_salt=user_password_salt,
        secret_key=user_secret_key
    )

    states = crudUser.create_user(user,session)
    if states == 0 :
        return {"message": "User created successfully"}
    else:
        raise HTTPException(status_code=400, detail="email already exists!")
