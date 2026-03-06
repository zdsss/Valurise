"""
Celery应用配置
用于异步任务处理
"""

from celery import Celery
from app.config import settings

# 创建Celery应用
celery_app = Celery(
    "valurise",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL
)

# Celery配置
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=600,  # 10分钟超时
    task_soft_time_limit=540,  # 9分钟软超时
    worker_prefetch_multiplier=1,  # 一次只取一个任务
    worker_max_tasks_per_child=50,  # 每个worker最多处理50个任务后重启
)

# 任务路由
celery_app.conf.task_routes = {
    "app.services.tasks.*": {"queue": "default"}
}
