"""
Celery异步任务
处理分析任务
"""

import asyncio
from datetime import datetime
from typing import Dict, Any
from sqlalchemy.orm import Session

from app.core.celery_app import celery_app
from app.database import SessionLocal
from app.models.analysis import Analysis
from app.services.agent_service import agent_service
from agents_optimized import AgentError


@celery_app.task(bind=True, name="app.services.tasks.process_analysis_task")
def process_analysis_task(self, analysis_id: str):
    """
    处理分析任务（Celery任务）

    Args:
        analysis_id: 分析任务ID
    """
    db: Session = SessionLocal()

    try:
        # 获取分析记录
        analysis = db.query(Analysis).filter(Analysis.id == analysis_id).first()
        if not analysis:
            raise Exception(f"分析任务不存在: {analysis_id}")

        # 更新状态为处理中
        analysis.status = "processing"
        analysis.started_at = datetime.utcnow()
        db.commit()

        # 准备输入数据
        input_data = analysis.input_data
        target_role = analysis.target_role

        # 构建原始输入文本
        raw_input = _build_raw_input(input_data)

        # 进度回调函数
        def progress_callback(current_step: int, total_steps: int, agent_name: str, message: str):
            """更新进度"""
            print(f"[{analysis_id}] Step {current_step}/{total_steps} - {agent_name}: {message}")
            # TODO: 可以通过WebSocket推送进度给前端

        # 调用Agent处理
        result = asyncio.run(
            agent_service.process_analysis(
                raw_input=raw_input,
                target_role=target_role,
                num_versions=input_data.get("options", {}).get("num_resume_versions", 1),
                progress_callback=progress_callback
            )
        )

        # 保存结果
        analysis.extracted_info = result.get("extracted_info")
        analysis.value_analysis = result.get("value_analysis")
        analysis.narrative_strategy = result.get("narrative_strategy")
        analysis.resume_versions = result.get("resume_versions")

        # 保存元数据
        metadata = result.get("metadata", {})
        analysis.cost = metadata.get("total_cost")
        analysis.processing_time_seconds = metadata.get("processing_time_seconds")

        # 更新状态为完成
        analysis.status = "completed"
        analysis.completed_at = datetime.utcnow()

        db.commit()

        return {
            "status": "completed",
            "analysis_id": analysis_id,
            "cost": float(analysis.cost) if analysis.cost else 0,
            "processing_time": analysis.processing_time_seconds
        }

    except AgentError as e:
        # Agent处理错误
        analysis.status = "failed"
        analysis.error_message = str(e)
        analysis.completed_at = datetime.utcnow()
        db.commit()

        raise Exception(f"Agent处理失败: {str(e)}")

    except Exception as e:
        # 其他错误
        analysis.status = "failed"
        analysis.error_message = str(e)
        analysis.completed_at = datetime.utcnow()
        db.commit()

        raise Exception(f"任务处理失败: {str(e)}")

    finally:
        db.close()


def _build_raw_input(input_data: Dict[str, Any]) -> str:
    """
    构建原始输入文本

    Args:
        input_data: 输入数据字典

    Returns:
        格式化的原始输入文本
    """
    parts = []

    # 添加原始文本
    if input_data.get("raw_text"):
        parts.append(input_data["raw_text"])
        parts.append("\n")

    # 添加工作经历
    work_experiences = input_data.get("work_experiences", [])
    if work_experiences:
        parts.append("工作经历：")
        for exp in work_experiences:
            parts.append(f"\n- {exp.get('start_date')} - {exp.get('end_date')}: {exp.get('company')}，{exp.get('position')}")
            if exp.get("responsibilities"):
                for resp in exp["responsibilities"]:
                    parts.append(f"  - {resp}")
            if exp.get("achievements"):
                for ach in exp["achievements"]:
                    parts.append(f"  - {ach}")
        parts.append("\n")

    # 添加教育背景
    education = input_data.get("education", [])
    if education:
        parts.append("教育背景：")
        for edu in education:
            parts.append(f"\n- {edu.get('institution')}，{edu.get('degree')}，{edu.get('field')}，{edu.get('graduation_date')}")
        parts.append("\n")

    # 添加技能
    skills = input_data.get("skills", [])
    if skills:
        parts.append("技能：")
        parts.append("\n- " + "、".join(skills))

    return "\n".join(parts)
