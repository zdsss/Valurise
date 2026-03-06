"""
Valurise MVP Prototype - Multi-Agent System
4个专业化Agent的实现
"""

import json
from typing import Dict, Any, List
from anthropic import Anthropic
from models import (
    UserProfile, TargetRole, ExtractedInfo, ValueAnalysis,
    NarrativeStrategy, ResumeVersion
)


class AgentBase:
    """Agent基类"""

    def __init__(self, client: Anthropic, model: str = "claude-sonnet-4-6"):
        self.client = client
        self.model = model
        self.cost = 0.0
        self.tokens_used = {"input": 0, "output": 0}

    def _calculate_cost(self, usage: Dict[str, int]) -> float:
        """计算API调用成本"""
        # Sonnet 4.6 pricing (2026)
        input_cost = usage.get("input_tokens", 0) * 0.000003  # $3/M tokens
        output_cost = usage.get("output_tokens", 0) * 0.000015  # $15/M tokens
        return input_cost + output_cost

    def _call_claude(self, system: str, user_message: str, response_model: Any = None) -> Dict[str, Any]:
        """调用Claude API"""
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
        self.cost += self._calculate_cost(usage)
        self.tokens_used["input"] += usage.get("input_tokens", 0)
        self.tokens_used["output"] += usage.get("output_tokens", 0)

        # 提取内容
        content = response.content[0].text

        if response_model:
            # 清理可能的markdown代码块标记
            content = content.strip()
            if content.startswith("```json"):
                content = content[7:]  # 移除 ```json
            elif content.startswith("```"):
                content = content[3:]  # 移除 ```
            if content.endswith("```"):
                content = content[:-3]  # 移除结尾的 ```
            content = content.strip()

            # 尝试解析JSON
            try:
                return json.loads(content)
            except json.JSONDecodeError as e:
                print(f"\n❌ JSON解析失败: {e}")
                print(f"原始响应内容:\n{content[:500]}")
                raise
        return {"text": content}


class InformationExtractionAgent(AgentBase):
    """Agent 1: 信息提取Agent

    职责：
    - 从用户输入中提取结构化信息
    - 识别缺失信息
    - 发现隐含的洞察
    """

    def extract(self, raw_input: str, target_role: TargetRole) -> ExtractedInfo:
        """提取用户信息"""

        system_prompt = """你是一个专业的信息提取专家。你的任务是从用户的原始输入中提取结构化的职业信息。

关键任务：
1. 提取基本信息（姓名、联系方式、教育、工作经历）
2. 识别技能、成就和项目经验
3. 发现用户可能没有明确表达但隐含的信息
4. 标记缺失的关键信息

注意：
- 保持客观，不要添加用户没有提供的信息
- 识别模糊或不完整的描述
- 注意时间线的连贯性
"""

        user_message = f"""请从以下用户输入中提取结构化信息：

用户输入：
{raw_input}

目标岗位：
- 职位：{target_role.title}
- 行业：{target_role.industry}
- 关键要求：{', '.join(target_role.key_requirements)}

请提取完整的用户档案，并标注：
1. 从输入中获得的额外洞察
2. 需要用户补充的信息（特别是与目标岗位相关的）
"""

        result = self._call_claude(system_prompt, user_message, ExtractedInfo)
        return ExtractedInfo(**result)


class ValueAnalysisAgent(AgentBase):
    """Agent 2: 价值分析Agent

    职责：
    - 识别和量化关键成就
    - 发现可迁移技能
    - 挖掘隐藏价值
    - 构建能力图谱
    """

    def analyze(self, profile: UserProfile, target_role: TargetRole) -> ValueAnalysis:
        """分析用户价值"""

        system_prompt = """你是一个资深的职业价值分析专家。你的任务是深度挖掘用户的职业价值。

核心任务：
1. **量化成就**：将模糊的成就转化为具体的、可量化的商业价值
   - 使用数字、百分比、规模来量化影响
   - 评估每个成就的影响力（1-10分）
   - 阐明商业价值（收入增长、成本节约、效率提升等）

2. **识别可迁移技能**：
   - 找出可以应用到目标岗位的技能
   - 提供具体证据
   - 评估与目标岗位的相关性（1-10分）
   - 给出定位建议（如何在简历中呈现）

3. **发现隐藏优势**：
   - 用户可能没有意识到但很有价值的经验
   - 跨领域的独特组合
   - 软技能和领导力证据

4. **构建能力图谱**：
   - 按领域分类用户的能力
   - 识别优势领域和成长领域

关键原则：
- 基于事实，不夸大
- 关注商业价值和影响力
- 考虑目标岗位的需求
- 发现用户的独特性
"""

        user_message = f"""请分析以下用户的职业价值：

用户档案：
{profile.model_dump_json(indent=2)}

目标岗位：
- 职位：{target_role.title}
- 行业：{target_role.industry}
- 关键要求：{', '.join(target_role.key_requirements)}

请提供：
1. 量化的关键成就（至少5个）
2. 可迁移技能分析（至少5个）
3. 独特价值主张（3-5个）
4. 隐藏优势（用户可能没意识到的）
5. 能力图谱
"""

        result = self._call_claude(system_prompt, user_message, ValueAnalysis)
        return ValueAnalysis(**result)


class NarrativeStrategyAgent(AgentBase):
    """Agent 3: 叙事策略Agent

    职责：
    - 构建职业故事
    - 设计叙事弧线
    - 制定定位策略
    - 确定差异化点
    """

    def strategize(
        self,
        profile: UserProfile,
        value_analysis: ValueAnalysis,
        target_role: TargetRole
    ) -> NarrativeStrategy:
        """制定叙事策略"""

        system_prompt = """你是一个职业叙事战略专家。你的任务是将用户的经历和价值编织成有说服力的职业故事。

核心任务：
1. **构建职业叙事**：
   - 创建一个连贯的、有说服力的职业发展故事
   - 解释职业转折和选择的逻辑
   - 展示成长轨迹和未来潜力

2. **设计故事弧线**：
   - 识别2-3个核心主题（如：技术创新、团队领导、商业增长）
   - 为每个主题构建叙事和支撑点
   - 确保故事与目标岗位相关

3. **定位陈述**：
   - 用1-2句话总结用户的独特定位
   - 清晰、有力、易记

4. **差异化策略**：
   - 识别用户与其他候选人的差异点
   - 强调独特的经验组合或视角

关键原则：
- 真实性：基于事实，不编造
- 相关性：与目标岗位高度相关
- 说服力：逻辑清晰，证据充分
- 独特性：突出用户的与众不同
"""

        user_message = f"""请为以下用户制定叙事策略：

用户档案：
{profile.model_dump_json(indent=2)}

价值分析：
{value_analysis.model_dump_json(indent=2)}

目标岗位：
- 职位：{target_role.title}
- 行业：{target_role.industry}
- 关键要求：{', '.join(target_role.key_requirements)}

请提供：
1. 整体职业叙事（200-300字）
2. 2-3个故事弧线（每个包含主题、叙事、支撑点）
3. 定位陈述（1-2句话）
4. 核心信息点（5-7个）
5. 差异化点（3-5个）
"""

        result = self._call_claude(system_prompt, user_message, NarrativeStrategy)
        return NarrativeStrategy(**result)


class ResumeFormattingAgent(AgentBase):
    """Agent 4: 简历格式化Agent

    职责：
    - 生成结构化简历
    - ATS优化
    - 多版本适配
    - 格式和可读性优化
    """

    def format_resume(
        self,
        profile: UserProfile,
        value_analysis: ValueAnalysis,
        narrative: NarrativeStrategy,
        target_role: TargetRole
    ) -> ResumeVersion:
        """生成简历版本"""

        system_prompt = """你是一个专业的简历优化专家。你的任务是将用户的价值和叙事转化为高质量的简历。

核心任务：
1. **结构化内容**：
   - 专业摘要（3-4句话，体现定位和价值）
   - 工作经历（使用STAR/CAR框架，突出成就）
   - 技能分类（技术技能、软技能、工具等）
   - 教育背景

2. **ATS优化**：
   - 提取关键词（从职位描述）
   - 确保关键词自然融入内容
   - 使用标准的section标题

3. **内容优化**：
   - 每个bullet point都应该展示价值（不只是职责）
   - 使用动作动词开头
   - 量化成果
   - 简洁有力（每个bullet 1-2行）

4. **针对性调整**：
   - 根据目标岗位调整重点
   - 突出最相关的经验和技能
   - 调整语言风格（技术 vs 商业）

关键原则：
- 清晰：易于扫描和理解
- 相关：与目标岗位高度匹配
- 有力：每句话都有价值
- 真实：不夸大或编造
"""

        user_message = f"""请为以下用户生成简历：

用户档案：
{profile.model_dump_json(indent=2)}

价值分析：
{value_analysis.model_dump_json(indent=2)}

叙事策略：
{narrative.model_dump_json(indent=2)}

目标岗位：
- 职位：{target_role.title}
- 行业：{target_role.industry}
- 关键要求：{', '.join(target_role.key_requirements)}

请生成：
1. 专业摘要
2. 优化的工作经历（每个职位3-5个bullet points）
3. 分类的技能section
4. 教育背景
5. 其他相关section（如项目、认证等）
6. ATS关键词列表
7. 优化建议
"""

        result = self._call_claude(system_prompt, user_message, ResumeVersion)
        return ResumeVersion(**result)


class ValuriseOrchestrator:
    """多Agent编排器

    协调4个Agent的工作流程
    """

    def __init__(self, api_key: str, model_main: str = "claude-sonnet-4-6", base_url: str = None):
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

    def process(
        self,
        raw_input: str,
        target_role: TargetRole,
        num_versions: int = 1
    ) -> Dict[str, Any]:
        """执行完整的多Agent流程"""

        import time
        start_time = time.time()

        # Step 1: 信息提取
        print("🔍 Agent 1: 提取用户信息...")
        extracted = self.extraction_agent.extract(raw_input, target_role)
        print(f"   ✓ 完成 (成本: ${self.extraction_agent.cost:.4f})")

        # Step 2: 价值分析
        print("💎 Agent 2: 分析职业价值...")
        value_analysis = self.value_agent.analyze(
            extracted.structured_profile,
            target_role
        )
        print(f"   ✓ 完成 (成本: ${self.value_agent.cost:.4f})")

        # Step 3: 叙事策略
        print("📖 Agent 3: 制定叙事策略...")
        narrative = self.narrative_agent.strategize(
            extracted.structured_profile,
            value_analysis,
            target_role
        )
        print(f"   ✓ 完成 (成本: ${self.narrative_agent.cost:.4f})")

        # Step 4: 生成简历
        print(f"📄 Agent 4: 生成简历版本...")
        resume_versions = []
        for i in range(num_versions):
            resume = self.formatting_agent.format_resume(
                extracted.structured_profile,
                value_analysis,
                narrative,
                target_role
            )
            resume_versions.append(resume)
        print(f"   ✓ 完成 (成本: ${self.formatting_agent.cost:.4f})")

        # 计算总成本和时间
        total_cost = (
            self.extraction_agent.cost +
            self.value_agent.cost +
            self.narrative_agent.cost +
            self.formatting_agent.cost
        )
        processing_time = time.time() - start_time

        cost_breakdown = {
            "extraction": self.extraction_agent.cost,
            "value_analysis": self.value_agent.cost,
            "narrative": self.narrative_agent.cost,
            "formatting": self.formatting_agent.cost
        }

        print(f"\n✅ 处理完成!")
        print(f"   总成本: ${total_cost:.4f}")
        print(f"   处理时间: {processing_time:.2f}秒")
        print(f"   成本目标: {'✓ 达成' if total_cost < 2.0 else '✗ 超出'} (目标<$2.00)")

        return {
            "extracted_info": extracted,
            "value_analysis": value_analysis,
            "narrative_strategy": narrative,
            "resume_versions": resume_versions,
            "cost_breakdown": cost_breakdown,
            "total_cost": total_cost,
            "processing_time": processing_time
        }
