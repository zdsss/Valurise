"""
分析任务模型
"""

import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Integer, Text, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship

from app.database import Base


class Analysis(Base):
    """分析任务表"""

    __tablename__ = "analyses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    status = Column(String(20), default="pending", nullable=False, index=True)
    # pending, processing, completed, failed

    # 输入数据
    input_data = Column(JSONB, nullable=False)
    target_role = Column(JSONB, nullable=False)

    # 输出数据
    extracted_info = Column(JSONB)
    value_analysis = Column(JSONB)
    narrative_strategy = Column(JSONB)
    resume_versions = Column(JSONB)

    # 元数据
    cost = Column(Numeric(10, 4))
    processing_time_seconds = Column(Integer)
    error_message = Column(Text)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    started_at = Column(DateTime)
    completed_at = Column(DateTime)

    # 关系
    user = relationship("User", back_populates="analyses")
    order = relationship("Order", back_populates="analysis", uselist=False)

    def __repr__(self):
        return f"<Analysis {self.id} - {self.status}>"
