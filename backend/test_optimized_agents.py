"""
测试优化后的Agent系统
验证重试机制、错误处理、性能改进
"""

import os
import json
import asyncio
from datetime import datetime
from dotenv import load_dotenv
from agents_optimized import ValuriseOrchestrator, AgentError

# 加载环境变量
load_dotenv()

# 测试数据
TEST_INPUT = """
我叫张伟，有5年的产品经理经验。

工作经历：
- 2021-至今：某互联网公司，高级产品经理
  - 负责AI助手产品线，从0到1搭建产品
  - 用户量从0增长到50万，月活30万
  - 主导产品策略，协调10人团队
  - 完成3轮融资路演，获得A轮投资

- 2019-2021：某创业公司，产品经理
  - 负责SaaS产品设计和迭代
  - 客户续费率提升至85%
  - 推动产品从MVP到商业化

教育背景：
- 北京大学，计算机科学学士，2019年毕业
- GPA 3.8/4.0

技能：
- 产品设计、用户研究、数据分析
- Figma, Axure, SQL, Python
- 敏捷开发、项目管理
"""

TARGET_ROLE = {
    "title": "AI产品总监",
    "industry": "人工智能/互联网",
    "key_requirements": [
        "5年以上产品经验",
        "AI产品经验",
        "团队管理经验",
        "数据驱动决策"
    ]
}


def progress_callback(current_step: int, total_steps: int, agent_name: str, message: str):
    """进度回调函数"""
    progress = (current_step / total_steps) * 100
    print(f"[{progress:.0f}%] Step {current_step}/{total_steps} - {agent_name}: {message}")


async def test_optimized_agents():
    """测试优化后的Agent系统"""
    print("=" * 60)
    print("测试优化后的Agent系统")
    print("=" * 60)

    # 获取API配置
    api_key = os.getenv("ANTHROPIC_API_KEY")
    base_url = os.getenv("ANTHROPIC_BASE_URL")

    if not api_key:
        print("❌ 错误: 未设置 ANTHROPIC_API_KEY 环境变量")
        return

    print(f"\n✅ API配置:")
    print(f"   - API Key: {api_key[:20]}...")
    print(f"   - Base URL: {base_url or 'Default'}")
    print(f"   - Model: claude-sonnet-4-6")

    # 初始化Orchestrator
    orchestrator = ValuriseOrchestrator(
        api_key=api_key,
        model_main="claude-sonnet-4-6",
        base_url=base_url
    )

    print(f"\n📝 测试输入:")
    print(f"   - 用户: 张伟")
    print(f"   - 目标岗位: {TARGET_ROLE['title']}")
    print(f"   - 输入长度: {len(TEST_INPUT)} 字符")

    # 开始处理
    start_time = datetime.now()
    print(f"\n⏱️  开始时间: {start_time.strftime('%H:%M:%S')}")
    print("\n" + "=" * 60)

    try:
        # 异步处理
        result = await orchestrator.process_async(
            raw_input=TEST_INPUT,
            target_role=TARGET_ROLE,
            num_versions=1,
            progress_callback=progress_callback
        )

        end_time = datetime.now()
        processing_time = (end_time - start_time).total_seconds()

        print("\n" + "=" * 60)
        print("✅ 处理成功!")
        print("=" * 60)

        # 输出统计信息
        metadata = result.get("metadata", {})
        print(f"\n📊 性能指标:")
        print(f"   - 处理时间: {processing_time:.1f}秒 ({processing_time/60:.2f}分钟)")
        print(f"   - 总成本: ${metadata.get('total_cost', 0):.4f}")
        print(f"   - 完成时间: {end_time.strftime('%H:%M:%S')}")

        # Agent统计
        print(f"\n📈 Agent统计:")
        for stats in metadata.get("agent_stats", []):
            print(f"\n   {stats['agent']}:")
            print(f"      - API调用次数: {stats['call_count']}")
            print(f"      - 错误次数: {stats['error_count']}")
            print(f"      - 成本: ${stats['cost']:.4f}")
            print(f"      - Token使用: {stats['tokens_used']['input']} in / {stats['tokens_used']['output']} out")

        # 输出结果摘要
        print(f"\n📄 结果摘要:")

        extracted = result.get("extracted_info", {})
        if isinstance(extracted, dict) and "text" in extracted:
            text = extracted["text"]
            print(f"   - 信息提取: {len(text)} 字符")
            print(f"     预览: {text[:100]}...")

        value = result.get("value_analysis", {})
        if isinstance(value, dict) and "text" in value:
            text = value["text"]
            print(f"   - 价值分析: {len(text)} 字符")
            print(f"     预览: {text[:100]}...")

        narrative = result.get("narrative_strategy", {})
        if isinstance(narrative, dict) and "text" in narrative:
            text = narrative["text"]
            print(f"   - 叙事策略: {len(text)} 字符")
            print(f"     预览: {text[:100]}...")

        resume_versions = result.get("resume_versions", [])
        print(f"   - 简历版本: {len(resume_versions)} 个")

        # 保存完整结果
        output_file = f"test_results/optimized_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        os.makedirs("test_results", exist_ok=True)

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        print(f"\n💾 完整结果已保存到: {output_file}")

        # 性能评估
        print(f"\n🎯 性能评估:")
        target_time = 120  # 2分钟目标
        target_cost = 0.50

        time_status = "✅" if processing_time < target_time else "⚠️"
        cost_status = "✅" if metadata.get('total_cost', 0) < target_cost else "⚠️"

        print(f"   {time_status} 处理时间: {processing_time:.1f}s (目标: <{target_time}s)")
        print(f"   {cost_status} 成本: ${metadata.get('total_cost', 0):.4f} (目标: <${target_cost})")

        if processing_time < target_time and metadata.get('total_cost', 0) < target_cost:
            print(f"\n🎉 所有性能指标达标!")
        else:
            print(f"\n⚠️  部分指标需要继续优化")

        return result

    except AgentError as e:
        print(f"\n❌ Agent处理失败: {e}")
        return None
    except Exception as e:
        print(f"\n❌ 未预期的错误: {e}")
        import traceback
        traceback.print_exc()
        return None


async def test_retry_mechanism():
    """测试重试机制（使用无效API key）"""
    print("\n" + "=" * 60)
    print("测试重试机制")
    print("=" * 60)

    # 使用无效的API key来触发重试
    orchestrator = ValuriseOrchestrator(
        api_key="sk-invalid-key-for-testing",
        model_main="claude-sonnet-4-6"
    )

    print("\n⚠️  使用无效API key测试重试机制...")

    try:
        result = await orchestrator.process_async(
            raw_input="测试输入",
            target_role={"title": "测试岗位", "industry": "测试", "key_requirements": []},
            num_versions=1
        )
        print("❌ 预期应该失败，但成功了")
    except Exception as e:
        print(f"✅ 按预期失败: {type(e).__name__}")
        print(f"   错误信息: {str(e)[:100]}...")


if __name__ == "__main__":
    print("\n🚀 开始测试优化后的Agent系统\n")

    # 测试1: 正常流程
    result = asyncio.run(test_optimized_agents())

    # 测试2: 重试机制（可选，会失败）
    # asyncio.run(test_retry_mechanism())

    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)
