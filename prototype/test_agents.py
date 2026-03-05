"""
Valurise MVP Prototype - Unit Tests
测试各个Agent的基本功能
"""

import pytest
from unittest.mock import Mock, patch
from models import UserProfile, TargetRole, WorkExperience, Education
from agents import (
    InformationExtractionAgent,
    ValueAnalysisAgent,
    NarrativeStrategyAgent,
    ResumeFormattingAgent
)


@pytest.fixture
def mock_anthropic_client():
    """Mock Anthropic client"""
    client = Mock()
    return client


@pytest.fixture
def sample_user_profile():
    """示例用户档案"""
    return UserProfile(
        name="张伟",
        email="zhangwei@example.com",
        work_experiences=[
            WorkExperience(
                company="某互联网公司",
                position="高级产品经理",
                start_date="2021-01",
                end_date="Present",
                responsibilities=[
                    "负责AI助手产品线",
                    "带领5人团队"
                ],
                achievements=[
                    "用户量从0增长到50万",
                    "完成3个版本迭代"
                ],
                technologies=["Python", "SQL"]
            )
        ],
        education=[
            Education(
                institution="北京大学",
                degree="学士",
                field="计算机科学",
                graduation_date="2019-06"
            )
        ],
        skills=["产品设计", "用户研究", "数据分析", "Python", "SQL"]
    )


@pytest.fixture
def sample_target_role():
    """示例目标岗位"""
    return TargetRole(
        title="AI产品总监",
        industry="人工智能",
        key_requirements=[
            "5年以上产品经验",
            "AI产品经验",
            "团队管理经验"
        ]
    )


class TestInformationExtractionAgent:
    """测试信息提取Agent"""

    def test_agent_initialization(self, mock_anthropic_client):
        """测试Agent初始化"""
        agent = InformationExtractionAgent(mock_anthropic_client)
        assert agent.client == mock_anthropic_client
        assert agent.cost == 0.0
        assert agent.tokens_used == {"input": 0, "output": 0}

    def test_cost_calculation(self, mock_anthropic_client):
        """测试成本计算"""
        agent = InformationExtractionAgent(mock_anthropic_client)

        usage = {
            "input_tokens": 1000,
            "output_tokens": 500
        }

        cost = agent._calculate_cost(usage)

        # Sonnet 4.6: $3/M input, $15/M output
        expected_cost = (1000 * 0.000003) + (500 * 0.000015)
        assert cost == pytest.approx(expected_cost)


class TestValueAnalysisAgent:
    """测试价值分析Agent"""

    def test_agent_initialization(self, mock_anthropic_client):
        """测试Agent初始化"""
        agent = ValueAnalysisAgent(mock_anthropic_client)
        assert agent.client == mock_anthropic_client
        assert agent.cost == 0.0


class TestNarrativeStrategyAgent:
    """测试叙事策略Agent"""

    def test_agent_initialization(self, mock_anthropic_client):
        """测试Agent初始化"""
        agent = NarrativeStrategyAgent(mock_anthropic_client)
        assert agent.client == mock_anthropic_client
        assert agent.cost == 0.0


class TestResumeFormattingAgent:
    """测试简历格式化Agent"""

    def test_agent_initialization(self, mock_anthropic_client):
        """测试Agent初始化"""
        agent = ResumeFormattingAgent(mock_anthropic_client)
        assert agent.client == mock_anthropic_client
        assert agent.cost == 0.0


class TestDataModels:
    """测试数据模型"""

    def test_user_profile_creation(self, sample_user_profile):
        """测试用户档案创建"""
        assert sample_user_profile.name == "张伟"
        assert len(sample_user_profile.work_experiences) == 1
        assert len(sample_user_profile.education) == 1
        assert len(sample_user_profile.skills) == 5

    def test_target_role_creation(self, sample_target_role):
        """测试目标岗位创建"""
        assert sample_target_role.title == "AI产品总监"
        assert sample_target_role.industry == "人工智能"
        assert len(sample_target_role.key_requirements) == 3

    def test_work_experience_serialization(self):
        """测试工作经历序列化"""
        exp = WorkExperience(
            company="Test Company",
            position="Product Manager",
            start_date="2020-01",
            end_date="2021-12",
            responsibilities=["Task 1", "Task 2"],
            achievements=["Achievement 1"]
        )

        data = exp.model_dump()
        assert data["company"] == "Test Company"
        assert len(data["responsibilities"]) == 2
        assert len(data["achievements"]) == 1


# 集成测试（需要真实API key，标记为skip）
@pytest.mark.skip(reason="需要真实API key")
class TestIntegration:
    """集成测试"""

    def test_full_pipeline(self):
        """测试完整流程"""
        # 这里需要真实的API key和完整的流程测试
        pass


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
