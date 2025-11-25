from fastapi import APIRouter,HTTPException
# from fastapi import HTTPException
from ..dependencies import requestModel,secureHelper
# from ..dependencies.datamodel import *
# from ..dependencies.responseModel import *
from ..crud.dbDependencies import SessionDep
# from ..crud import crudUser
from ..depends import get_logger
# from secrets import compare_digest
router = APIRouter()
logger = get_logger(__name__)

@router.post("/api/user/ban")
async def ban_user(data:requestModel.BanUser,session: SessionDep):
    pass

@router.post("/api/user/unban")
async def unban_user(data:requestModel.BanUser,session: SessionDep):
    pass

@router.post("/api/admin/ban")
async def ban_user(data:requestModel.BanUser,session: SessionDep):
    # id=0 的管理员有权完成
    pass

@router.post("/api/admin/unban")
async def unban_user(data:requestModel.BanUser,session: SessionDep):
    pass

@router.post("/api/resource/create")
async def create_resource(data:requestModel.CreateResource,session: SessionDep):
    # ResourceControl
    pass

@router.post("/api/resource/ban")
async def create_resource(data:requestModel.BanResource,session: SessionDep):
    pass

@router.post("/api/resource/unban")
async def unban_resource(data:requestModel.BanResource,session: SessionDep):
    pass

@router.post("/api/resource/addUser")
async def add_user(data:requestModel.AddUser,session: SessionDep):
    pass

@router.post("/api/resource/addAdmin")
async def add_admin(data:requestModel.AddAdmin,session: SessionDep):
    pass
