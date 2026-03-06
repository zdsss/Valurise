"""
Agent服务
封装Agent调用逻辑
"""

import sys
import os
from typing import Dict, Any, Optional, Callable
from datetime import datetime

# 添加backend目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from agents_optimized import ValuriseOrchestrator, AgentError
from app.config import settings


class AgentService:
    """Agent服务类"""

    def __init__(self):
        """初始化Agent服务"""
        self.orchestrator = ValuriseOrchestrator(
            api_key=settings.ANTHROPIC_API_KEY,
            model_main=settings.MODEL_MAIN,
            base_url=settings.ANTHROPIC_BASE_URL
        )

    async def process_analysis(
        self,
        raw_input: str,
        target_role: Dict[str, Any],
        num_versions: int = 1,
        progress_callback: Optional[Callable] = None
    ) -> Dict[str, Any]:
        """
        处理分析任务

        Args:
            raw_input: 原始输入文本
            target_role: 目标岗位信息
            num_versions: 简历版本数量
            progress_callback: 进度回调函数

        Returns:
            分析结果字典

        Raises:
            AgentError: Agent处理失败
        """
        try:
            result = await self.orchestrator.process_async(
                raw_input=raw_input,
                target_role=target_role,
                num_versions=num_versions,
                progress_callback=progress_callback
            )
            return result
        except AgentError as e:
            raise e
        except Exception as e:
            raise AgentError(f"Agent处理失败: {str(e)}")

    def get_total_cost(self) -> float:
        """获取总成本"""
        return self.orchestrator.get_total_cost()

    def get_all_stats(self) -> list:
        """获取所有Agent统计信息"""
        return self.orchestrator.get_all_stats()


# 创建全局Agent服务实例
agent_service = AgentService()
