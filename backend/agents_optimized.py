"""
Valurise Backend - Optimized Multi-Agent System
优化后的4个专业化Agent实现，支持重试、并行处理、错误处理
"""

import json
import asyncio
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
from anthropic import Anthropic, APIError, APIConnectionError, RateLimitError
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
    before_sleep_log
)

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AgentError(Exception):
    """Agent处理错误"""
    pass


class AgentBase:
    """Agent基类 - 优化版"""

    def __init__(
        self,
        client: Anthropic,
        model: str = "claude-sonnet-4-6",
        max_retries: int = 3
    ):
        self.client = client
        self.model = model
        self.max_retries = max_retries
        self.cost = 0.0
        self.tokens_used = {"input": 0, "output": 0}
        self.call_count = 0
        self.error_count = 0

    def _calculate_cost(self, usage: Dict[str, int]) -> float:
        """计算API调用成本"""
        # Sonnet 4.6 pricing (2026)
        input_cost = usage.get("input_tokens", 0) * 0.000003  # $3/M tokens
        output_cost = usage.get("output_tokens", 0) * 0.000015  # $15/M tokens
        return input_cost + output_cost

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=(
            retry_if_exception_type(APIConnectionError) |
            retry_if_exception_type(RateLimitError) |
            retry_if_exception_type(APIError)
        ),
        before_sleep=before_sleep_log(logger, logging.WARNING)
    )
    def _call_claude_with_retry(
        self,
        system: str,
        user_message: str,
        response_model: Any = None
    ) -> Dict[str, Any]:
        """调用Claude API（带重试机制）"""
        try:
            self.call_count += 1
            messages = [{"role": "user", "content": user_message}]

            # 如果指定了response_model，在system prompt中要求JSON输出
            if response_model:
                json_schema = response_model.model_json_schema()
                system_with_json = f"""{system}

IMPORTANT: You must respond with valid JSON that matches this schema:
{json.dumps(json_schema, indent=2)}

Respond ONLY with the JSON object, no additional text."""

                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=4096,
                    system=system_with_json,
                    messages=messages
                )
            else:
                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=4096,
                    system=system,
                    messages=messages
                )

            # 记录成本
            usage = response.usage.model_dump()
            cost = self._calculate_cost(usage)
            self.cost += cost
            self.tokens_used["input"] += usage.get("input_tokens", 0)
            self.tokens_used["output"] += usage.get("output_tokens", 0)

            logger.info(
                f"{self.__class__.__name__} API call successful. "
                f"Cost: ${cost:.4f}, "
                f"Tokens: {usage.get('input_tokens', 0)} in / "
                f"{usage.get('output_tokens', 0)} out"
            )

            # 提取内容
            content = response.content[0].text

            if response_model:
                # 清理可能的markdown代码块标记
                content = content.strip()
                if content.startswith("```json"):
                    content = content[7:]
                elif content.startswith("```"):
                    content = content[3:]
                if content.endswith("```"):
                    content = content[:-3]
                content = content.strip()

                # 尝试解析JSON
                try:
                    return json.loads(content)
                except json.JSONDecodeError as e:
                    logger.error(f"JSON解析失败: {e}")
                    logger.error(f"原始响应内容:\n{content[:500]}")
                    raise AgentError(f"JSON解析失败: {e}")

            return {"text": content}

        except (APIConnectionError, RateLimitError, APIError) as e:
            self.error_count += 1
            logger.error(f"API调用失败: {e}")
            raise  # 让retry装饰器处理重试

        except Exception as e:
            self.error_count += 1
            logger.error(f"未预期的错误: {e}")
            raise AgentError(f"Agent处理失败: {e}")

    def get_stats(self) -> Dict[str, Any]:
        """获取Agent统计信息"""
        return {
            "agent": self.__class__.__name__,
            "cost": self.cost,
            "tokens_used": self.tokens_used,
            "call_count": self.call_count,
            "error_count": self.error_count
        }


class InformationExtractionAgent(AgentBase):
    """Agent 1: 信息提取Agent（优化版）"""

    async def extract_async(
        self,
        raw_input: str,
        target_role: Dict[str, Any]
    ) -> Dict[str, Any]:
        """异步提取用户信息"""
        system_prompt = """你是一个专业的信息提取专家。你的任务是从用户的原始输入中提取结构化的职业信息。

关键任务：
1. 提取基本信息（姓名、联系方式）
2. 提取工作经历（公司、职位、时间、职责、成就）
3. 提取教育背景
4. 提取技能列表
5. 识别缺失的关键信息
6. 发现隐含的洞察

注意：
- 尽可能提取详细信息
- 对于缺失的信息，明确指出
- 对于模糊的信息，做出合理推断并标注
- 识别用户可能没有明确表达但隐含的优势"""

        user_message = f"""请从以下用户输入中提取结构化信息：

用户输入：
{raw_input}

目标岗位：
- 职位：{target_role.get('title', '')}
- 行业：{target_role.get('industry', '')}
- 关键要求：{', '.join(target_role.get('key_requirements', []))}

请提取完整的结构化信息。"""

        # 注意：这里使用同步调用，因为Anthropic SDK不支持async
        # 在实际部署中，可以使用线程池来实现并发
        result = self._call_claude_with_retry(
            system_prompt,
            user_message,
            response_model=None  # 暂时返回字典，后续可以添加Pydantic模型
        )

        return result

    def extract(
        self,
        raw_input: str,
        target_role: Dict[str, Any]
    ) -> Dict[str, Any]:
        """同步提取用户信息（兼容旧接口）"""
        return asyncio.run(self.extract_async(raw_input, target_role))


class ValueAnalysisAgent(AgentBase):
    """Agent 2: 价值分析Agent（优化版）"""

    async def analyze_async(
        self,
        extracted_info: Dict[str, Any],
        target_role: Dict[str, Any]
    ) -> Dict[str, Any]:
        """异步分析职业价值"""
        system_prompt = """你是一个资深的职业价值分析专家。你的任务是深度挖掘候选人的职业价值。

关键任务：
1. 量化关键成就（用数据说话）
2. 识别可迁移技能（评估与目标岗位的相关性）
3. 发现独特价值主张（差异化优势）
4. 识别隐藏优势（候选人可能没意识到的）
5. 构建能力图谱（全面展示能力结构）

分析原则：
- 每个成就都要量化商业价值
- 技能要评估可迁移性（1-10分）
- 价值主张要具体、可验证
- 发现候选人的独特竞争优势"""

        user_message = f"""请分析以下候选人的职业价值：

提取的信息：
{json.dumps(extracted_info, ensure_ascii=False, indent=2)}

目标岗位：
- 职位：{target_role.get('title', '')}
- 行业：{target_role.get('industry', '')}
- 关键要求：{', '.join(target_role.get('key_requirements', []))}

请进行深度价值分析。"""

        result = self._call_claude_with_retry(
            system_prompt,
            user_message,
            response_model=None
        )

        return result

    def analyze(
        self,
        extracted_info: Dict[str, Any],
        target_role: Dict[str, Any]
    ) -> Dict[str, Any]:
        """同步分析职业价值（兼容旧接口）"""
        return asyncio.run(self.analyze_async(extracted_info, target_role))


class NarrativeStrategyAgent(AgentBase):
    """Agent 3: 叙事策略Agent（优化版）"""

    async def create_async(
        self,
        extracted_info: Dict[str, Any],
        value_analysis: Dict[str, Any],
        target_role: Dict[str, Any]
    ) -> Dict[str, Any]:
        """异步创建叙事策略"""
        system_prompt = """你是一个职业叙事策略专家。你的任务是帮助候选人构建有说服力的职业故事。

关键任务：
1. 构建职业叙事（完整的职业发展故事）
2. 设计故事弧线（3-5个核心故事）
3. 制定定位陈述（一句话价值主张）
4. 提炼关键信息（核心卖点）
5. 明确差异化点（与竞争者的区别）

叙事原则：
- 故事要真实、连贯、有说服力
- 突出成长轨迹和价值创造
- 与目标岗位高度相关
- 展现独特性和不可替代性"""

        user_message = f"""请为以下候选人制定叙事策略：

提取的信息：
{json.dumps(extracted_info, ensure_ascii=False, indent=2)[:1000]}...

价值分析：
{json.dumps(value_analysis, ensure_ascii=False, indent=2)[:1000]}...

目标岗位：
- 职位：{target_role.get('title', '')}
- 行业：{target_role.get('industry', '')}

请创建完整的叙事策略。"""

        result = self._call_claude_with_retry(
            system_prompt,
            user_message,
            response_model=None
        )

        return result

    def create(
        self,
        extracted_info: Dict[str, Any],
        value_analysis: Dict[str, Any],
        target_role: Dict[str, Any]
    ) -> Dict[str, Any]:
        """同步创建叙事策略（兼容旧接口）"""
        return asyncio.run(
            self.create_async(extracted_info, value_analysis, target_role)
        )


class ResumeFormattingAgent(AgentBase):
    """Agent 4: 简历格式化Agent（优化版）"""

    async def format_async(
        self,
        extracted_info: Dict[str, Any],
        value_analysis: Dict[str, Any],
        narrative_strategy: Dict[str, Any],
        target_role: Dict[str, Any],
        num_versions: int = 1
    ) -> List[Dict[str, Any]]:
        """异步生成简历版本"""
        system_prompt = """你是一个专业的简历优化专家。你的任务是生成优化的简历内容。

关键任务：
1. 撰写专业摘要（Professional Summary）
2. 优化工作经历描述（突出成就和影响）
3. 组织技能部分（按相关性排序）
4. 添加ATS关键词（提高通过率）
5. 提供优化建议

优化原则：
- 每个bullet point都要展现价值
- 使用行动动词开头
- 量化成果（数据、百分比）
- 针对目标岗位定制
- ATS友好（关键词优化）"""

        user_message = f"""请生成优化的简历内容：

提取的信息：
{json.dumps(extracted_info, ensure_ascii=False, indent=2)[:800]}...

价值分析：
{json.dumps(value_analysis, ensure_ascii=False, indent=2)[:800]}...

叙事策略：
{json.dumps(narrative_strategy, ensure_ascii=False, indent=2)[:800]}...

目标岗位：
- 职位：{target_role.get('title', '')}
- 行业：{target_role.get('industry', '')}

请生成{num_versions}个简历版本。"""

        result = self._call_claude_with_retry(
            system_prompt,
            user_message,
            response_model=None
        )

        # 确保返回列表格式
        if isinstance(result, dict) and "text" in result:
            return [result]
        elif isinstance(result, list):
            return result
        else:
            return [result]

    def format(
        self,
        extracted_info: Dict[str, Any],
        value_analysis: Dict[str, Any],
        narrative_strategy: Dict[str, Any],
        target_role: Dict[str, Any],
        num_versions: int = 1
    ) -> List[Dict[str, Any]]:
        """同步生成简历版本（兼容旧接口）"""
        return asyncio.run(
            self.format_async(
                extracted_info,
                value_analysis,
                narrative_strategy,
                target_role,
                num_versions
            )
        )


class ValuriseOrchestrator:
    """多Agent编排器（优化版）

    支持：
    - 并行处理（部分Agent可并行）
    - 错误处理和重试
    - 进度回调
    - 成本追踪
    """

    def __init__(
        self,
        api_key: str,
        model_main: str = "claude-sonnet-4-6",
        base_url: Optional[str] = None
    ):
        if base_url:
            self.client = Anthropic(api_key=api_key, base_url=base_url)
        else:
            self.client = Anthropic(api_key=api_key)

        self.model = model_main

        # 初始化4个Agent
        self.extraction_agent = InformationExtractionAgent(self.client, self.model)
        self.value_agent = ValueAnalysisAgent(self.client, self.model)
        self.narrative_agent = NarrativeStrategyAgent(self.client, self.model)
        self.formatting_agent = ResumeFormattingAgent(self.client, self.model)

    async def process_async(
        self,
        raw_input: str,
        target_role: Dict[str, Any],
        num_versions: int = 1,
        progress_callback: Optional[callable] = None
    ) -> Dict[str, Any]:
        """异步处理（支持并行）"""
        start_time = datetime.now()

        try:
            # Step 1: 信息提取（必须先完成）
            if progress_callback:
                progress_callback(1, 4, "extraction", "正在提取用户信息...")

            logger.info("Step 1: 信息提取...")
            extracted = await self.extraction_agent.extract_async(
                raw_input,
                target_role
            )

            # Step 2-3: 价值分析和叙事策略可以并行
            if progress_callback:
                progress_callback(2, 4, "value_analysis", "正在分析职业价值...")

            logger.info("Step 2-3: 价值分析和叙事策略（并行）...")

            # 注意：由于Anthropic SDK不支持真正的async，这里仍然是顺序执行
            # 在生产环境中，可以使用线程池实现真正的并行
            value_task = self.value_agent.analyze_async(extracted, target_role)
            narrative_task = self.narrative_agent.create_async(
                extracted,
                {},  # 暂时传空，实际可以传部分value结果
                target_role
            )

            # 等待两个任务完成
            value, narrative = await asyncio.gather(value_task, narrative_task)

            # Step 4: 简历格式化（依赖前面的结果）
            if progress_callback:
                progress_callback(4, 4, "formatting", "正在生成简历...")

            logger.info("Step 4: 简历格式化...")
            resume_versions = await self.formatting_agent.format_async(
                extracted,
                value,
                narrative,
                target_role,
                num_versions
            )

            # 计算总成本和时间
            end_time = datetime.now()
            processing_time = (end_time - start_time).total_seconds()

            total_cost = (
                self.extraction_agent.cost +
                self.value_agent.cost +
                self.narrative_agent.cost +
                self.formatting_agent.cost
            )

            result = {
                "extracted_info": extracted,
                "value_analysis": value,
                "narrative_strategy": narrative,
                "resume_versions": resume_versions,
                "metadata": {
                    "total_cost": total_cost,
                    "processing_time_seconds": processing_time,
                    "agent_stats": [
                        self.extraction_agent.get_stats(),
                        self.value_agent.get_stats(),
                        self.narrative_agent.get_stats(),
                        self.formatting_agent.get_stats()
                    ],
                    "completed_at": end_time.isoformat()
                }
            }

            logger.info(
                f"处理完成！总成本: ${total_cost:.4f}, "
                f"处理时间: {processing_time:.1f}秒"
            )

            return result

        except Exception as e:
            logger.error(f"处理失败: {e}")
            raise AgentError(f"多Agent处理失败: {e}")

    def process(
        self,
        raw_input: str,
        target_role: Dict[str, Any],
        num_versions: int = 1,
        progress_callback: Optional[callable] = None
    ) -> Dict[str, Any]:
        """同步处理（兼容旧接口）"""
        return asyncio.run(
            self.process_async(
                raw_input,
                target_role,
                num_versions,
                progress_callback
            )
        )

    def get_total_cost(self) -> float:
        """获取总成本"""
        return (
            self.extraction_agent.cost +
            self.value_agent.cost +
            self.narrative_agent.cost +
            self.formatting_agent.cost
        )

    def get_all_stats(self) -> List[Dict[str, Any]]:
        """获取所有Agent的统计信息"""
        return [
            self.extraction_agent.get_stats(),
            self.value_agent.get_stats(),
            self.narrative_agent.get_stats(),
            self.formatting_agent.get_stats()
        ]
