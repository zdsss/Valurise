"""
订单和支付相关的Pydantic schemas
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, UUID4, HttpUrl


# 创建支付会话请求
class CreateCheckoutRequest(BaseModel):
    """创建支付会话请求"""
    product_tier: str = Field(..., pattern="^(basic|pro|premium)$")
    success_url: HttpUrl
    cancel_url: HttpUrl


# 创建支付会话响应
class CreateCheckoutResponse(BaseModel):
    """创建支付会话响应"""
    checkout_session_id: str
    checkout_url: str
    order_id: UUID4


# 支付验证响应
class PaymentVerifyResponse(BaseModel):
    """支付验证响应"""
    order_id: UUID4
    status: str
    product_tier: str
    amount_cents: int
    paid_at: Optional[datetime] = None
    analysis_id: Optional[UUID4] = None

    model_config = {"from_attributes": True}


# Webhook响应
class WebhookResponse(BaseModel):
    """Webhook响应"""
    received: bool = True


# 订单响应
class OrderResponse(BaseModel):
    """订单响应"""
    id: UUID4
    user_id: UUID4
    product_tier: str
    amount_cents: int
    currency: str
    status: str
    created_at: datetime
    paid_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
