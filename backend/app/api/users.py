"""
用户相关API
获取和更新用户信息
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.models.user import User
from app.models.analysis import Analysis
from app.models.order import Order
from app.schemas.user import UserDetail, UserUpdate, UserStats
from app.api.deps import get_current_active_user

router = APIRouter()


@router.get("/me", response_model=UserDetail)
async def get_current_user_info(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    获取当前用户信息

    返回用户基本信息和统计数据
    """
    # 查询统计信息
    total_analyses = db.query(func.count(Analysis.id)).filter(
        Analysis.user_id == current_user.id
    ).scalar() or 0

    completed_analyses = db.query(func.count(Analysis.id)).filter(
        Analysis.user_id == current_user.id,
        Analysis.status == "completed"
    ).scalar() or 0

    total_spent = db.query(func.sum(Order.amount_cents)).filter(
        Order.user_id == current_user.id,
        Order.status == "paid"
    ).scalar() or 0

    # 构建响应
    stats = UserStats(
        total_analyses=total_analyses,
        completed_analyses=completed_analyses,
        total_spent_cents=int(total_spent)
    )

    return UserDetail(
        id=current_user.id,
        email=current_user.email,
        full_name=current_user.full_name,
        subscription_tier=current_user.subscription_tier,
        credits_remaining=current_user.credits_remaining,
        created_at=current_user.created_at,
        is_active=current_user.is_active,
        is_verified=current_user.is_verified,
        stats=stats
    )


@router.patch("/me", response_model=UserDetail)
async def update_current_user(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    更新当前用户信息

    - **full_name**: 全名（可选）
    """
    # 更新用户信息
    if user_update.full_name is not None:
        current_user.full_name = user_update.full_name

    db.commit()
    db.refresh(current_user)

    # 查询统计信息
    total_analyses = db.query(func.count(Analysis.id)).filter(
        Analysis.user_id == current_user.id
    ).scalar() or 0

    completed_analyses = db.query(func.count(Analysis.id)).filter(
        Analysis.user_id == current_user.id,
        Analysis.status == "completed"
    ).scalar() or 0

    total_spent = db.query(func.sum(Order.amount_cents)).filter(
        Order.user_id == current_user.id,
        Order.status == "paid"
    ).scalar() or 0

    stats = UserStats(
        total_analyses=total_analyses,
        completed_analyses=completed_analyses,
        total_spent_cents=int(total_spent)
    )

    return UserDetail(
        id=current_user.id,
        email=current_user.email,
        full_name=current_user.full_name,
        subscription_tier=current_user.subscription_tier,
        credits_remaining=current_user.credits_remaining,
        created_at=current_user.created_at,
        is_active=current_user.is_active,
        is_verified=current_user.is_verified,
        stats=stats
    )
