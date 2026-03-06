"""
分析相关API
创建分析任务、查询状态、获取结果
"""

from datetime import datetime, timedelta
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.database import get_db
from app.models.user import User
from app.models.analysis import Analysis
from app.schemas.analysis import (
    AnalysisCreate,
    AnalysisCreateResponse,
    AnalysisStatus,
    AnalysisResultResponse,
    AnalysisResult,
    AnalysisMetadata,
    AnalysisHistoryResponse,
    AnalysisHistoryItem
)
from app.api.deps import get_current_active_user
from app.services.tasks import process_analysis_task

router = APIRouter()


@router.post("", response_model=AnalysisCreateResponse, status_code=status.HTTP_202_ACCEPTED)
async def create_analysis(
    analysis_data: AnalysisCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    创建分析任务

    - **input_data**: 输入数据（工作经历、教育背景、技能等）
    - **target_role**: 目标岗位信息
    - **options**: 分析选项（简历版本数量等）

    返回分析任务ID和预估处理时间
    """
    # 检查用户是否有足够的积分
    if current_user.credits_remaining <= 0:
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail="积分不足，请先购买"
        )

    # 创建分析记录
    new_analysis = Analysis(
        user_id=current_user.id,
        status="pending",
        input_data={
            "raw_text": analysis_data.input_data.raw_text,
            "work_experiences": [exp.model_dump() for exp in analysis_data.input_data.work_experiences],
            "education": [edu.model_dump() for edu in analysis_data.input_data.education],
            "skills": analysis_data.input_data.skills,
            "options": analysis_data.options.model_dump() if analysis_data.options else {}
        },
        target_role={
            "title": analysis_data.target_role.title,
            "industry": analysis_data.target_role.industry,
            "key_requirements": analysis_data.target_role.key_requirements
        }
    )

    db.add(new_analysis)
    db.commit()
    db.refresh(new_analysis)

    # 扣除积分
    current_user.credits_remaining -= 1
    db.commit()

    # 提交Celery任务
    process_analysis_task.delay(str(new_analysis.id))

    # 预估处理时间（2分钟）
    estimated_time = 120

    return AnalysisCreateResponse(
        analysis_id=new_analysis.id,
        status=new_analysis.status,
        estimated_time_seconds=estimated_time,
        created_at=new_analysis.created_at
    )


@router.get("/{analysis_id}", response_model=AnalysisStatus)
async def get_analysis_status(
    analysis_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    获取分析任务状态

    返回任务状态和进度信息
    """
    # 查询分析记录
    analysis = db.query(Analysis).filter(
        Analysis.id == analysis_id,
        Analysis.user_id == current_user.id
    ).first()

    if not analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="分析任务不存在"
        )

    # 计算预估完成时间
    estimated_completion = None
    if analysis.status == "processing" and analysis.started_at:
        # 假设处理时间为2分钟
        estimated_completion = analysis.started_at + timedelta(seconds=120)

    return AnalysisStatus(
        id=analysis.id,
        status=analysis.status,
        progress=None,  # TODO: 实现实时进度
        created_at=analysis.created_at,
        started_at=analysis.started_at,
        estimated_completion=estimated_completion
    )


@router.get("/{analysis_id}/result", response_model=AnalysisResultResponse)
async def get_analysis_result(
    analysis_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    获取分析结果

    只有状态为completed的任务才能获取结果
    """
    # 查询分析记录
    analysis = db.query(Analysis).filter(
        Analysis.id == analysis_id,
        Analysis.user_id == current_user.id
    ).first()

    if not analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="分析任务不存在"
        )

    # 检查状态
    if analysis.status != "completed":
        raise HTTPException(
            status_code=status.HTTP_425_TOO_EARLY,
            detail=f"分析任务尚未完成，当前状态: {analysis.status}"
        )

    # 构建结果
    result = AnalysisResult(
        extracted_info=analysis.extracted_info or {},
        value_analysis=analysis.value_analysis or {},
        narrative_strategy=analysis.narrative_strategy or {},
        resume_versions=analysis.resume_versions or []
    )

    metadata = AnalysisMetadata(
        cost=float(analysis.cost) if analysis.cost else 0.0,
        processing_time_seconds=analysis.processing_time_seconds or 0,
        completed_at=analysis.completed_at
    )

    return AnalysisResultResponse(
        id=analysis.id,
        status=analysis.status,
        result=result,
        metadata=metadata
    )


@router.get("", response_model=AnalysisHistoryResponse)
async def get_analysis_history(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=50),
    status_filter: Optional[str] = Query(None, alias="status"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    获取分析历史

    - **page**: 页码（从1开始）
    - **limit**: 每页数量（1-50）
    - **status**: 状态过滤（可选）

    返回分析历史列表和分页信息
    """
    # 构建查询
    query = db.query(Analysis).filter(Analysis.user_id == current_user.id)

    # 状态过滤
    if status_filter:
        query = query.filter(Analysis.status == status_filter)

    # 总数
    total = query.count()

    # 分页
    offset = (page - 1) * limit
    analyses = query.order_by(desc(Analysis.created_at)).offset(offset).limit(limit).all()

    # 构建历史项
    history_items = []
    for analysis in analyses:
        target_role_title = analysis.target_role.get("title", "未知岗位")
        history_items.append(
            AnalysisHistoryItem(
                id=analysis.id,
                status=analysis.status,
                target_role=target_role_title,
                created_at=analysis.created_at,
                completed_at=analysis.completed_at,
                cost=float(analysis.cost) if analysis.cost else None
            )
        )

    # 分页信息
    total_pages = (total + limit - 1) // limit
    pagination = {
        "page": page,
        "limit": limit,
        "total": total,
        "total_pages": total_pages
    }

    return AnalysisHistoryResponse(
        analyses=history_items,
        pagination=pagination
    )
