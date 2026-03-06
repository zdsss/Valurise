"""
模拟用户测试数据生成器
基于市场调研和产品特点，生成合理的模拟用户反馈
用于决策分析和产品优化
"""

import json
import random
from datetime import datetime, timedelta
from pathlib import Path

# 模拟用户数据
SIMULATED_USERS = [
    {
        "user_name": "张明",
        "background": "5年后端工程师，想转产品经理",
        "test_date": "2026-03-06",
        "scores": {
            "extraction": 5,
            "value_analysis": 5,
            "narrative": 4,
            "resume": 5,
            "overall": 5
        },
        "willing_to_pay": 1,  # 是，我会付费
        "price_point": 3,  # $99
        "nps_score": 9,
        "feedback": {
            "best_feature": "价值分析太棒了！发现了我自己都没意识到的优势，特别是把技术经验转化为产品价值的部分",
            "improvement": "处理时间有点长，希望能更快一些。另外希望能生成多个版本的简历",
            "other": "这个工具解决了我最大的痛点 - 不知道如何重新定位自己。强烈推荐给想转型的朋友！"
        }
    },
    {
        "user_name": "李娜",
        "background": "6年运营经理，准备晋升运营总监",
        "test_date": "2026-03-07",
        "scores": {
            "extraction": 4,
            "value_analysis": 5,
            "narrative": 5,
            "resume": 4,
            "overall": 5
        },
        "willing_to_pay": 1,
        "price_point": 4,  # $199
        "nps_score": 10,
        "feedback": {
            "best_feature": "叙事策略部分非常专业！帮我构建了从执行到战略的完整故事，这正是我晋升需要的",
            "improvement": "希望能针对不同公司文化定制简历版本",
            "other": "物超所值！比我之前花$300找的职业咨询师还要专业。已经推荐给3个同事了"
        }
    },
    {
        "user_name": "王浩",
        "background": "应届毕业生，找数据分析师工作",
        "test_date": "2026-03-07",
        "scores": {
            "extraction": 4,
            "value_analysis": 4,
            "narrative": 4,
            "resume": 5,
            "overall": 4
        },
        "willing_to_pay": 2,  # 可能会，取决于价格
        "price_point": 2,  # $49
        "nps_score": 8,
        "feedback": {
            "best_feature": "把我的实习经历和项目经验量化了，看起来很有说服力。简历格式也很专业",
            "improvement": "对应届生来说$99有点贵，希望有学生优惠",
            "other": "很有帮助，但作为应届生预算有限。如果能便宜一些会更好"
        }
    },
    {
        "user_name": "陈总",
        "background": "12年技术管理经验，寻找CTO机会",
        "test_date": "2026-03-08",
        "scores": {
            "extraction": 5,
            "value_analysis": 5,
            "narrative": 5,
            "resume": 5,
            "overall": 5
        },
        "willing_to_pay": 1,
        "price_point": 4,  # $199
        "nps_score": 10,
        "feedback": {
            "best_feature": "战略思维和业务影响力的分析非常到位，完全是高管级别的定位。商业价值量化做得很专业",
            "improvement": "希望能增加LinkedIn优化和高管个人品牌建设的建议",
            "other": "这个价格太值了！我之前咨询过猎头，收费$500+还没这么深入。会推荐给我的高管朋友们"
        }
    },
    {
        "user_name": "赵敏",
        "background": "7年供应链管理，传统制造业转互联网",
        "test_date": "2026-03-08",
        "scores": {
            "extraction": 4,
            "value_analysis": 5,
            "narrative": 5,
            "resume": 4,
            "overall": 5
        },
        "willing_to_pay": 1,
        "price_point": 3,  # $99
        "nps_score": 9,
        "feedback": {
            "best_feature": "可迁移技能识别太有用了！帮我把传统行业经验转化为互联网公司看重的能力，这是我最担心的问题",
            "improvement": "希望能提供更多行业转型的案例参考",
            "other": "解决了我的核心痛点。跨行业转型最难的就是不知道如何表达自己的价值，这个工具做到了"
        }
    },
    {
        "user_name": "刘强",
        "background": "4年产品经理，想进大厂",
        "test_date": "2026-03-09",
        "scores": {
            "extraction": 4,
            "value_analysis": 4,
            "narrative": 4,
            "resume": 4,
            "overall": 4
        },
        "willing_to_pay": 1,
        "price_point": 3,  # $99
        "nps_score": 8,
        "feedback": {
            "best_feature": "成就量化做得很好，把我的产品成果都转化成了具体的数据",
            "improvement": "希望能针对不同大厂（阿里、腾讯、字节）的风格定制简历",
            "other": "整体很满意，输出质量高。$99的价格可以接受"
        }
    },
    {
        "user_name": "孙莉",
        "background": "3年UI设计师，想转UX设计",
        "test_date": "2026-03-09",
        "scores": {
            "extraction": 4,
            "value_analysis": 4,
            "narrative": 4,
            "resume": 4,
            "overall": 4
        },
        "willing_to_pay": 2,  # 可能会
        "price_point": 2,  # $49
        "nps_score": 7,
        "feedback": {
            "best_feature": "帮我识别了UI到UX的可迁移技能，这个角度很有用",
            "improvement": "对设计师来说，希望简历能更有设计感。另外价格有点高",
            "other": "内容不错，但感觉$99对我来说有点贵。如果$49会更容易接受"
        }
    },
    {
        "user_name": "周杰",
        "background": "8年销售经理，想转商务拓展",
        "test_date": "2026-03-10",
        "scores": {
            "extraction": 5,
            "value_analysis": 5,
            "narrative": 4,
            "resume": 4,
            "overall": 5
        },
        "willing_to_pay": 1,
        "price_point": 3,  # $99
        "nps_score": 9,
        "feedback": {
            "best_feature": "价值分析非常专业，把我的销售业绩转化为商务拓展能力，角度很独特",
            "improvement": "希望能提供面试准备的建议",
            "other": "非常满意！这个工具帮我理清了职业转型的思路。会推荐给团队的同事"
        }
    }
]


def generate_simulated_feedback():
    """生成模拟用户反馈数据"""

    data = {
        "users": SIMULATED_USERS,
        "summary": {},
        "metadata": {
            "generated_at": datetime.now().isoformat(),
            "note": "这是基于市场调研和产品特点生成的模拟数据，用于决策分析",
            "assumptions": [
                "目标用户（职业转型者、晋升候选人）满意度高（4-5分）",
                "应届生和初级职场人对价格更敏感",
                "高管和资深专家愿意支付更高价格",
                "整体NPS预期在40-50之间",
                "付费意愿预期60-70%"
            ]
        }
    }

    # 计算汇总指标
    n = len(SIMULATED_USERS)

    # 平均满意度
    avg_satisfaction = sum(u["scores"]["overall"] for u in SIMULATED_USERS) / n

    # 付费意愿
    willing_users = sum(1 for u in SIMULATED_USERS if u["willing_to_pay"] <= 2)
    willing_percentage = (willing_users / n) * 100

    # 愿意支付$99
    willing_99 = sum(1 for u in SIMULATED_USERS if u["price_point"] >= 3)
    willing_99_percentage = (willing_99 / n) * 100

    # NPS
    promoters = sum(1 for u in SIMULATED_USERS if u["nps_score"] >= 9)
    passives = sum(1 for u in SIMULATED_USERS if 7 <= u["nps_score"] <= 8)
    detractors = sum(1 for u in SIMULATED_USERS if u["nps_score"] <= 6)
    nps = ((promoters - detractors) / n) * 100

    # 各项评分
    avg_extraction = sum(u["scores"]["extraction"] for u in SIMULATED_USERS) / n
    avg_value = sum(u["scores"]["value_analysis"] for u in SIMULATED_USERS) / n
    avg_narrative = sum(u["scores"]["narrative"] for u in SIMULATED_USERS) / n
    avg_resume = sum(u["scores"]["resume"] for u in SIMULATED_USERS) / n

    data["summary"] = {
        "total_users": n,
        "avg_satisfaction": avg_satisfaction,
        "willing_to_pay_percentage": willing_percentage,
        "willing_99_percentage": willing_99_percentage,
        "nps": nps,
        "nps_breakdown": {
            "promoters": promoters,
            "passives": passives,
            "detractors": detractors
        },
        "avg_scores": {
            "extraction": avg_extraction,
            "value_analysis": avg_value,
            "narrative": avg_narrative,
            "resume": avg_resume
        }
    }

    return data


def save_simulated_data():
    """保存模拟数据"""
    data = generate_simulated_feedback()

    output_file = Path("user_feedback_data.json")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"✓ 模拟数据已生成: {output_file}")
    print(f"\n关键指标:")
    print(f"  测试用户数: {data['summary']['total_users']}")
    print(f"  平均满意度: {data['summary']['avg_satisfaction']:.2f}/5")
    print(f"  付费意愿: {data['summary']['willing_to_pay_percentage']:.1f}%")
    print(f"  愿意支付$99: {data['summary']['willing_99_percentage']:.1f}%")
    print(f"  NPS评分: {data['summary']['nps']:.1f}")

    return data


if __name__ == "__main__":
    save_simulated_data()
