"""
分析相关的Pydantic schemas
"""

from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field, UUID4


# 工作经历
class WorkExperience(BaseModel):
    """工作经历"""
    company: str = Field(..., min_length=1, max_length=100)
    position: str = Field(..., min_length=1, max_length=100)
    start_date: str  # YYYY-MM 或 "present"
    end_date: str  # YYYY-MM 或 "present"
    responsibilities: List[str] = []
    achievements: List[str] = []


# 教育背景
class Education(BaseModel):
    """教育背景"""
    institution: str = Field(..., min_length=1, max_length=100)
    degree: str = Field(..., min_length=1, max_length=50)
    field: str = Field(..., min_length=1, max_length=100)
    graduation_date: str  # YYYY or YYYY-MM


# 目标岗位
class TargetRole(BaseModel):
    """目标岗位"""
    title: str = Field(..., min_length=1, max_length=100)
    industry: str = Field(..., min_length=1, max_length=100)
    key_requirements: List[str] = []


# 分析输入数据
class AnalysisInput(BaseModel):
    """分析输入数据"""
    raw_text: Optional[str] = None
    work_experiences: List[WorkExperience] = []
    education: List[Education] = []
    skills: List[str] = []


# 分析选项
class AnalysisOptions(BaseModel):
    """分析选项"""
    num_resume_versions: int = Field(1, ge=1, le=5)
    include_linkedin: bool = False


# 创建分析请求
class AnalysisCreate(BaseModel):
    """创建分析请求"""
    input_data: AnalysisInput
    target_role: TargetRole
    options: Optional[AnalysisOptions] = AnalysisOptions()


# 分析进度
class AnalysisProgress(BaseModel):
    """分析进度"""
    current_step: int
    total_steps: int
    current_agent: str
    message: str
    progress_percentage: int


# 分析状态响应
class AnalysisStatus(BaseModel):
    """分析状态响应"""
    id: UUID4
    status: str
    progress: Optional[AnalysisProgress] = None
    created_at: datetime
    started_at: Optional[datetime] = None
    estimated_completion: Optional[datetime] = None

    model_config = {"from_attributes": True}


# 分析结果
class AnalysisResult(BaseModel):
    """分析结果"""
    extracted_info: Dict[str, Any]
    value_analysis: Dict[str, Any]
    narrative_strategy: Dict[str, Any]
    resume_versions: List[Dict[str, Any]]


# 分析元数据
class AnalysisMetadata(BaseModel):
    """分析元数据"""
    cost: float
    processing_time_seconds: int
    completed_at: datetime


# 完整分析结果响应
class AnalysisResultResponse(BaseModel):
    """完整分析结果响应"""
    id: UUID4
    status: str
    result: AnalysisResult
    metadata: AnalysisMetadata

    model_config = {"from_attributes": True}


# 分析创建响应
class AnalysisCreateResponse(BaseModel):
    """分析创建响应"""
    analysis_id: UUID4
    status: str
    estimated_time_seconds: int
    created_at: datetime


# 分析历史项
class AnalysisHistoryItem(BaseModel):
    """分析历史项"""
    id: UUID4
    status: str
    target_role: str
    created_at: datetime
    completed_at: Optional[datetime] = None
    cost: Optional[float] = None

    model_config = {"from_attributes": True}


# 分析历史响应
class AnalysisHistoryResponse(BaseModel):
    """分析历史响应"""
    analyses: List[AnalysisHistoryItem]
    pagination: Dict[str, Any]
