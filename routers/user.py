from fastapi import APIRouter
from ..dependencies import requestModel
from ..crud.dbDependencies import SessionDep
router = APIRouter()

@router.post("/api/user/login")
async def user_login(data:requestModel.UserLogin):
    user_email = data.email
    return {"user_email":user_email}

@router.get("/test/dependency")
async def test_dependency(session: SessionDep):
    return {
        "session_works": session is not None,
        "session_type": type(session).__name__
    }
