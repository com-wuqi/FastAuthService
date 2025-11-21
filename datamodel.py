from typing import List
from sqlmodel import Field, SQLModel

"""
数据库模型
"""

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=False, nullable=False)
    email: str = Field(index=True)
    password: str = Field(index=True)
    password_salt: str = Field(index=True,nullable=False)
    is_active: bool = Field(default=False)
    # 是否存活
    secret_key: str = Field(index=False)
    # 凭据

class AdminUser(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=False, nullable=False)
    email: str = Field(index=True)
    password: str = Field(index=True)
    password_salt: str = Field(index=True,nullable=False)
    is_active: bool = Field(default=False)
    secret_key: str = Field(index=False)
    is_superuser: bool = Field(default=False) # 最高权限

class ResourceControl(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    resource_name: str = Field(index=True)
    users: List[User.id] = Field(default_factory=list)
    admins: List[AdminUser.id] = Field(default_factory=list)
    operations: List[str] = Field(default_factory=list)
    # 可以执行的操作类型
    is_active: bool = Field(default=True)
    # 资源默认启用