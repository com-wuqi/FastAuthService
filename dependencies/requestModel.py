from pydantic import BaseModel
"""
请求体模型
"""
class UserLogin(BaseModel):
    email: str
    password: str

class UserRegister(BaseModel):
    email: str
    name: str
    password: str
    password_salt: str

class UserLogout(BaseModel):
    email: str
    password: str

class AdminLogin(UserLogin):
    pass

class AdminLogout(UserLogout):
    pass

class AdminRegister(UserRegister):
    is_superuser: bool
    # 最高权限

class ResourceAccess(BaseModel):
    payload: str
    # 从中获取 'resource_id':int 'operation':str 'other_data':str
    # other_data: str = None
    # # 其他必要数据，交由鉴权后处理模块对对应资源处理
    id: int
    is_admin: bool
    # 判断用户类型，用于获取 secret_key 鉴权，这样就不需要用户密码了

