"""
用户相关的Pydantic schemas
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, UUID4


# 用户注册
class UserRegister(BaseModel):
    """用户注册请求"""
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)
    full_name: Optional[str] = Field(None, max_length=100)


# 用户登录
class UserLogin(BaseModel):
    """用户登录请求"""
    email: EmailStr
    password: str


# Token响应
class Token(BaseModel):
    """Token响应"""
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str = "bearer"


# 用户信息（响应）
class UserResponse(BaseModel):
    """用户信息响应"""
    id: UUID4
    email: str
    full_name: Optional[str]
    subscription_tier: str
    credits_remaining: int
    created_at: datetime
    is_active: bool
    is_verified: bool

    model_config = {"from_attributes": True}


# 用户统计
class UserStats(BaseModel):
    """用户统计信息"""
    total_analyses: int
    completed_analyses: int
    total_spent_cents: int


# 用户详细信息（包含统计）
class UserDetail(UserResponse):
    """用户详细信息（包含统计）"""
    stats: UserStats


# 用户更新
class UserUpdate(BaseModel):
    """用户信息更新"""
    full_name: Optional[str] = Field(None, max_length=100)


# 注册响应
class UserRegisterResponse(BaseModel):
    """注册响应"""
    user: UserResponse
    access_token: str
    token_type: str = "bearer"


# 登录响应
class UserLoginResponse(BaseModel):
    """登录响应"""
    user: UserResponse
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
