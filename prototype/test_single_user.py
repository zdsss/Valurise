"""
单个用户测试脚本
用于测试单个用户的职业信息
"""

import os
import json
import time
from pathlib import Path
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich import print as rprint

from models import TargetRole
from agents import ValuriseOrchestrator

console = Console()


def get_user_input():
    """获取用户输入"""
    console.print("[bold cyan]请输入用户的职业信息[/bold cyan]")
    console.print("[dim]（输入完成后，单独一行输入 'END' 结束）[/dim]\n")

    lines = []
    while True:
        line = input()
        if line.strip() == "END":
            break
        lines.append(line)

    return "\n".join(lines)


def get_target_role():
    """获取目标岗位信息"""
    console.print("\n[bold cyan]请输入目标岗位信息[/bold cyan]")

    title = input("目标岗位: ")
    industry = input("目标行业: ")

    console.print("\n关键要求（每行一个，输入空行结束）:")
    requirements = []
    while True:
        req = input("  - ")
        if not req.strip():
            break
        requirements.append(req)

    return TargetRole(
        title=title,
        industry=industry,
        key_requirements=requirements
    )


def save_results(results, user_name):
    """保存测试结果"""
    output_dir = Path("user_test_results")
    output_dir.mkdir(exist_ok=True)

    # 生成文件名
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    filename = f"{user_name}_{timestamp}.json"
    output_file = output_dir / filename

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2, default=str)

    return output_file


def display_results(results):
    """显示测试结果摘要"""
    console.print("\n" + "="*60)
    console.print("[bold green]测试完成！[/bold green]")
    console.print("="*60 + "\n")

    # 成本和时间
    console.print(f"💰 成本: ${results['total_cost']:.4f}")
    console.print(f"⏱️  时间: {results['processing_time']:.1f}秒")

    # 信息提取
    extracted = results['extraction']
    profile = extracted['structured_profile']
    console.print(f"\n📋 提取信息:")
    console.print(f"  - 工作经历: {len(profile['work_experiences'])}段")
    console.print(f"  - 教育背景: {len(profile['education'])}个")
    console.print(f"  - 技能: {len(profile['skills'])}项")

    # 价值分析
    value = results['value_analysis']
    console.print(f"\n💎 价值分析:")
    console.print(f"  - 关键成就: {len(value['key_achievements'])}个")
    console.print(f"  - 可迁移技能: {len(value['transferable_skills'])}项")

    # 叙事策略
    narrative = results['narrative_strategy']
    console.print(f"\n📖 叙事策略:")
    console.print(f"  - 定位陈述: {narrative['positioning_statement'][:50]}...")
    console.print(f"  - 故事弧线: {len(narrative['story_arcs'])}个")

    console.print(f"\n✅ 详细结果已保存")


def main():
    """主函数"""
    console.print(Panel.fit(
        "[bold cyan]Valurise 用户测试工具[/bold cyan]\n"
        "单个用户职业价值分析",
        border_style="cyan"
    ))

    # 加载环境变量
    load_dotenv()
    api_key = os.getenv("ANTHROPIC_API_KEY")
    base_url = os.getenv("ANTHROPIC_BASE_URL")

    if not api_key:
        console.print("[red]错误: 未找到ANTHROPIC_API_KEY[/red]")
        return

    # 获取用户信息
    console.print("\n[bold]Step 1: 输入用户信息[/bold]")
    user_name = input("用户姓名/昵称: ")

    console.print("\n[bold]Step 2: 输入职业信息[/bold]")
    console.print("[dim]提示: 可以直接粘贴简历内容或职业描述[/dim]")
    user_input = get_user_input()

    console.print("\n[bold]Step 3: 输入目标岗位[/bold]")
    target_role = get_target_role()

    # 确认信息
    console.print("\n" + "="*60)
    console.print("[bold]请确认信息:[/bold]")
    console.print(f"用户: {user_name}")
    console.print(f"目标岗位: {target_role.title}")
    console.print(f"目标行业: {target_role.industry}")
    console.print(f"输入长度: {len(user_input)}字符")
    console.print("="*60)

    confirm = input("\n确认开始分析？(y/n): ")
    if confirm.lower() != 'y':
        console.print("[yellow]已取消[/yellow]")
        return

    # 初始化系统
    console.print("\n[bold]初始化AI系统...[/bold]")
    orchestrator = ValuriseOrchestrator(
        api_key=api_key,
        model_main=os.getenv("MODEL_MAIN", "claude-sonnet-4-6"),
        base_url=base_url
    )

    # 运行分析
    console.print("\n[bold]开始分析...[/bold]")
    console.print("[dim]这可能需要3-5分钟，请耐心等待...[/dim]\n")

    try:
        results = orchestrator.process(
            raw_input=user_input,
            target_role=target_role,
            num_versions=1
        )

        # 显示结果
        display_results(results)

        # 保存结果
        output_file = save_results(results, user_name)
        console.print(f"📁 文件位置: {output_file}")

        # 提示下一步
        console.print("\n[bold cyan]下一步:[/bold cyan]")
        console.print("1. 将结果发送给用户")
        console.print("2. 请用户填写反馈问卷 (user_feedback_form.md)")
        console.print("3. 将反馈记录到测试日志 (test_log.md)")

    except Exception as e:
        console.print(f"\n[red]❌ 分析失败: {e}[/red]")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
