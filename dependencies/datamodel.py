from typing import List
from datetime import datetime,timezone

from pygments.lexer import default
from sqlmodel import Field, SQLModel,Relationship,JSON,Column

"""
数据库模型
"""

class UserBase(SQLModel):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(index=False, nullable=False)
    email: str = Field(index=True,unique=True)
    password: str = Field(index=True)
    # 永远不要存储用户的明文密码，也不要在响应中发送密码。
    password_salt: str = Field(index=True, nullable=False)
    is_active: bool = Field(default=False)
    # 是否存活
    last_login: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
    secret_key: str = Field(index=False)
    # 凭据
    # 用户拥有的资源权限

class User(UserBase, table=True):
    __tablename__ = "user"
    user_resource_permissions: List["ResourcePermission"] = Relationship(
        back_populates="user"
    )

class AdminUser(UserBase, table=True):
    __tablename__ = "adminuser"
    is_superuser: bool = Field(default=False) # 最高权限
    admin_resource_permissions: List["ResourcePermission"] = Relationship(
        back_populates="admin"
    )

class ResourceControl(SQLModel, table=True):
    __tablename__ = "resourcecontrol"
    id: int | None = Field(default=None, primary_key=True)
    resource_name: str = Field(index=True)
    operations: List[str] = Field(default_factory=list,sa_column=Column(JSON))
    # 可以执行的操作类型
    is_active: bool = Field(default=True)
    # 资源默认启用
    permissions: List["ResourcePermission"] = Relationship(back_populates="resource")


class ResourcePermission(SQLModel, table=True):
    __tablename__ = "resourcepermission"
    id: int | None = Field(default=None, primary_key=True)
    # 关联到 User（可为空，因为权限可能属于普通用户或管理员）
    user_id: int | None = Field(default=None, foreign_key="user.id")
    # 关联到 AdminUser（可为空，因为权限可能属于普通用户或管理员）
    admin_id: int | None = Field(default=None, foreign_key="adminuser.id")
    # 关联到 ResourceControl
    resource_id: int = Field(foreign_key="resourcecontrol.id")
    # 权限级别或具体操作权限
    permission_level: str = Field(default="r")
    # 关系定义
    user: User = Relationship(back_populates="user_resource_permissions")
    admin: AdminUser = Relationship(back_populates="admin_resource_permissions")
    resource: ResourceControl = Relationship(back_populates="permissions")
