"""
Valurise MVP Prototype - Data Models
定义用户输入、Agent输出和最终结果的数据结构
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime


class WorkExperience(BaseModel):
    """工作经历"""
    company: str
    position: str
    start_date: str
    end_date: Optional[str] = "Present"
    responsibilities: List[str] = Field(default_factory=list)
    achievements: List[str] = Field(default_factory=list)
    technologies: List[str] = Field(default_factory=list)


class Education(BaseModel):
    """教育背景"""
    institution: str
    degree: str
    field: str
    graduation_date: str
    gpa: Optional[str] = None
    honors: List[str] = Field(default_factory=list)


class UserProfile(BaseModel):
    """用户基础信息"""
    name: str
    email: str
    phone: Optional[str] = None
    linkedin: Optional[str] = None
    summary: Optional[str] = None
    work_experiences: List[WorkExperience] = Field(default_factory=list)
    education: List[Education] = Field(default_factory=list)
    skills: List[str] = Field(default_factory=list)
    certifications: List[str] = Field(default_factory=list)
    languages: List[str] = Field(default_factory=list)


class TargetRole(BaseModel):
    """目标岗位"""
    title: str
    industry: str
    company_type: Optional[str] = None  # startup, enterprise, etc.
    key_requirements: List[str] = Field(default_factory=list)


# Agent 输出模型

class ExtractedInfo(BaseModel):
    """Agent 1: 信息提取结果"""
    structured_profile: UserProfile
    raw_insights: List[str] = Field(
        default_factory=list,
        description="从用户输入中提取的额外洞察"
    )
    missing_info: List[str] = Field(
        default_factory=list,
        description="需要用户补充的信息"
    )


class ValueAnalysis(BaseModel):
    """Agent 2: 价值分析结果"""

    class Achievement(BaseModel):
        original: str
        quantified: str
        impact_score: int = Field(ge=1, le=10)
        business_value: str

    class TransferableSkill(BaseModel):
        skill: str
        evidence: List[str]
        target_relevance: int = Field(ge=1, le=10)
        positioning: str

    key_achievements: List[Achievement] = Field(default_factory=list)
    transferable_skills: List[TransferableSkill] = Field(default_factory=list)
    unique_value_props: List[str] = Field(
        default_factory=list,
        description="用户的独特价值主张"
    )
    hidden_strengths: List[str] = Field(
        default_factory=list,
        description="用户未意识到的优势"
    )
    capability_map: Dict[str, List[str]] = Field(
        default_factory=dict,
        description="能力图谱：领域 -> 具体能力"
    )


class NarrativeStrategy(BaseModel):
    """Agent 3: 叙事策略结果"""

    class StoryArc(BaseModel):
        theme: str
        narrative: str
        supporting_points: List[str]

    career_narrative: str = Field(description="整体职业故事")
    story_arcs: List[StoryArc] = Field(default_factory=list)
    positioning_statement: str = Field(description="定位陈述")
    key_messages: List[str] = Field(
        default_factory=list,
        description="核心信息点"
    )
    differentiation_points: List[str] = Field(
        default_factory=list,
        description="与竞争者的差异化"
    )


class ResumeVersion(BaseModel):
    """Agent 4: 格式化简历版本"""
    target_role: str
    summary: str
    work_experiences: List[Dict[str, Any]]
    skills_section: Dict[str, List[str]]
    education: List[Dict[str, Any]]
    additional_sections: Dict[str, List[str]] = Field(default_factory=dict)
    ats_keywords: List[str] = Field(default_factory=list)
    optimization_notes: List[str] = Field(default_factory=list)


class ValuriseOutput(BaseModel):
    """最终输出"""
    user_id: str
    created_at: datetime = Field(default_factory=datetime.now)

    # Agent 输出
    extracted_info: ExtractedInfo
    value_analysis: ValueAnalysis
    narrative_strategy: NarrativeStrategy
    resume_versions: List[ResumeVersion] = Field(default_factory=list)

    # 元数据
    cost_breakdown: Dict[str, float] = Field(
        default_factory=dict,
        description="各Agent的成本"
    )
    total_cost: float = 0.0
    processing_time: float = 0.0

    # 用户反馈
    user_rating: Optional[int] = Field(None, ge=1, le=5)
    user_feedback: Optional[str] = None
