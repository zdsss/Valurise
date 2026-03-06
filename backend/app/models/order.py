"""
订单模型
"""

import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database import Base


class Order(Base):
    """订单表"""

    __tablename__ = "orders"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    analysis_id = Column(UUID(as_uuid=True), ForeignKey("analyses.id", ondelete="SET NULL"))

    # Stripe相关
    stripe_checkout_session_id = Column(String(255), unique=True, index=True)
    stripe_payment_intent_id = Column(String(255))

    # 订单信息
    product_tier = Column(String(20), nullable=False)
    # basic, pro, premium
    amount_cents = Column(Integer, nullable=False)
    currency = Column(String(3), default="USD", nullable=False)
    status = Column(String(20), default="pending", nullable=False, index=True)
    # pending, paid, failed, refunded

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    paid_at = Column(DateTime)

    # 关系
    user = relationship("User", back_populates="orders")
    analysis = relationship("Analysis", back_populates="order")

    def __repr__(self):
        return f"<Order {self.id} - {self.status}>"
