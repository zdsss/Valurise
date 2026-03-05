"""
Valurise MVP Prototype - CLI Interface
命令行界面，用于测试多Agent系统
"""

import os
import json
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.table import Table
from rich import print as rprint

from models import TargetRole, ValuriseOutput
from agents import ValuriseOrchestrator


console = Console()


def load_example_input() -> str:
    """加载示例用户输入"""
    return """
我叫张伟，有5年的产品经理经验。

工作经历：
1. 2021-现在：某互联网公司 - 高级产品经理
   - 负责AI助手产品线，从0到1搭建
   - 用户量从0增长到50万
   - 带领5人团队，完成3个版本迭代
   - 与技术团队紧密合作，推动AI功能落地

2. 2019-2021：某创业公司 - 产品经理
   - 负责B端SaaS产品
   - 完成产品重构，用户满意度提升30%
   - 参与融资路演，帮助公司获得A轮融资

教育：
- 2015-2019：北京大学 - 计算机科学学士

技能：
- 产品设计、用户研究、数据分析
- Python基础、SQL
- Figma、Axure

我现在想转型做AI产品总监，希望进入大厂或者有潜力的AI创业公司。
"""


def display_extraction_results(extracted):
    """显示信息提取结果"""
    console.print("\n[bold cyan]📋 信息提取结果[/bold cyan]")

    # 基本信息
    profile = extracted.structured_profile
    table = Table(show_header=False, box=None)
    table.add_row("姓名", profile.name)
    table.add_row("邮箱", profile.email or "未提供")
    table.add_row("工作经历", f"{len(profile.work_experiences)}段")
    table.add_row("教育背景", f"{len(profile.education)}个")
    table.add_row("技能", f"{len(profile.skills)}项")

    console.print(Panel(table, title="基本信息", border_style="cyan"))

    # 缺失信息
    if extracted.missing_info:
        console.print("\n[yellow]⚠️  需要补充的信息：[/yellow]")
        for info in extracted.missing_info:
            console.print(f"  • {info}")


def display_value_analysis(analysis):
    """显示价值分析结果"""
    console.print("\n[bold green]💎 价值分析结果[/bold green]")

    # 关键成就
    console.print("\n[bold]关键成就（量化）：[/bold]")
    for i, achievement in enumerate(analysis.key_achievements[:3], 1):
        console.print(f"\n{i}. [cyan]{achievement.original}[/cyan]")
        console.print(f"   → {achievement.quantified}")
        console.print(f"   影响力: {'⭐' * achievement.impact_score}")
        console.print(f"   商业价值: {achievement.business_value}")

    # 可迁移技能
    console.print("\n[bold]可迁移技能（Top 3）：[/bold]")
    top_skills = sorted(
        analysis.transferable_skills,
        key=lambda x: x.target_relevance,
        reverse=True
    )[:3]

    for skill in top_skills:
        console.print(f"\n• [green]{skill.skill}[/green] (相关性: {skill.target_relevance}/10)")
        console.print(f"  定位建议: {skill.positioning}")

    # 独特价值主张
    console.print("\n[bold]独特价值主张：[/bold]")
    for uvp in analysis.unique_value_props:
        console.print(f"  • {uvp}")


def display_narrative_strategy(narrative):
    """显示叙事策略结果"""
    console.print("\n[bold magenta]📖 叙事策略[/bold magenta]")

    # 定位陈述
    console.print(Panel(
        narrative.positioning_statement,
        title="定位陈述",
        border_style="magenta"
    ))

    # 职业叙事
    console.print("\n[bold]职业叙事：[/bold]")
    console.print(Markdown(narrative.career_narrative))

    # 故事弧线
    console.print("\n[bold]故事弧线：[/bold]")
    for arc in narrative.story_arcs:
        console.print(f"\n• [cyan]{arc.theme}[/cyan]")
        console.print(f"  {arc.narrative}")


def display_resume(resume):
    """显示简历版本"""
    console.print(f"\n[bold blue]📄 简历版本 - {resume.target_role}[/bold blue]")

    # 专业摘要
    console.print("\n[bold]Professional Summary:[/bold]")
    console.print(Panel(resume.summary, border_style="blue"))

    # 工作经历（显示第一段）
    if resume.work_experiences:
        console.print("\n[bold]Work Experience (示例):[/bold]")
        exp = resume.work_experiences[0]
        console.print(f"\n[cyan]{exp.get('position')} at {exp.get('company')}[/cyan]")
        for bullet in exp.get('bullets', [])[:3]:
            console.print(f"  • {bullet}")

    # ATS关键词
    console.print("\n[bold]ATS关键词：[/bold]")
    console.print(", ".join(resume.ats_keywords[:10]))


def display_cost_breakdown(cost_breakdown, total_cost, target=2.0):
    """显示成本分析"""
    console.print("\n[bold yellow]💰 成本分析[/bold yellow]")

    table = Table(show_header=True, header_style="bold yellow")
    table.add_column("Agent", style="cyan")
    table.add_column("成本", justify="right")
    table.add_column("占比", justify="right")

    for agent, cost in cost_breakdown.items():
        percentage = (cost / total_cost * 100) if total_cost > 0 else 0
        table.add_row(
            agent.replace("_", " ").title(),
            f"${cost:.4f}",
            f"{percentage:.1f}%"
        )

    table.add_row(
        "[bold]总计[/bold]",
        f"[bold]${total_cost:.4f}[/bold]",
        "[bold]100%[/bold]"
    )

    console.print(table)

    # 目标达成情况
    if total_cost < target:
        console.print(f"\n✅ 成本控制良好！低于目标 ${target:.2f}")
    else:
        console.print(f"\n⚠️  成本超出目标 ${target:.2f}，需要优化")


def save_results(results: dict, output_dir: Path):
    """保存结果到文件"""
    output_dir.mkdir(parents=True, exist_ok=True)

    # 保存完整结果（JSON）
    output_file = output_dir / "valurise_output.json"

    # 转换为可序列化的格式
    serializable_results = {
        "extracted_info": results["extracted_info"].model_dump(),
        "value_analysis": results["value_analysis"].model_dump(),
        "narrative_strategy": results["narrative_strategy"].model_dump(),
        "resume_versions": [r.model_dump() for r in results["resume_versions"]],
        "cost_breakdown": results["cost_breakdown"],
        "total_cost": results["total_cost"],
        "processing_time": results["processing_time"]
    }

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(serializable_results, f, ensure_ascii=False, indent=2)

    console.print(f"\n💾 结果已保存到: {output_file}")


def main():
    """主函数"""
    console.print(Panel.fit(
        "[bold cyan]Valurise MVP Prototype[/bold cyan]\n"
        "AI-Powered Career Value Discovery Engine",
        border_style="cyan"
    ))

    # 加载环境变量
    load_dotenv()
    api_key = os.getenv("ANTHROPIC_API_KEY")

    if not api_key:
        console.print("[red]错误: 未找到ANTHROPIC_API_KEY[/red]")
        console.print("请创建.env文件并设置API key")
        return

    # 加载示例输入
    console.print("\n[bold]使用示例用户输入...[/bold]")
    user_input = load_example_input()
    console.print(Panel(user_input[:200] + "...", title="用户输入（预览）", border_style="dim"))

    # 定义目标岗位
    target_role = TargetRole(
        title="AI产品总监",
        industry="人工智能/互联网",
        key_requirements=[
            "5年以上产品经验",
            "AI产品经验",
            "团队管理经验",
            "数据驱动决策",
            "技术背景"
        ]
    )

    console.print(f"\n[bold]目标岗位:[/bold] {target_role.title}")
    console.print(f"[bold]行业:[/bold] {target_role.industry}")

    # 初始化Orchestrator
    console.print("\n[bold]初始化多Agent系统...[/bold]")
    orchestrator = ValuriseOrchestrator(
        api_key=api_key,
        model_main=os.getenv("MODEL_MAIN", "claude-sonnet-4-6")
    )

    # 执行处理
    console.print("\n" + "="*60)
    console.print("[bold green]开始处理...[/bold green]")
    console.print("="*60 + "\n")

    try:
        results = orchestrator.process(
            raw_input=user_input,
            target_role=target_role,
            num_versions=1
        )

        # 显示结果
        console.print("\n" + "="*60)
        console.print("[bold green]处理结果[/bold green]")
        console.print("="*60)

        display_extraction_results(results["extracted_info"])
        display_value_analysis(results["value_analysis"])
        display_narrative_strategy(results["narrative_strategy"])

        for resume in results["resume_versions"]:
            display_resume(resume)

        display_cost_breakdown(
            results["cost_breakdown"],
            results["total_cost"],
            target=float(os.getenv("TARGET_COST_PER_RUN", "2.0"))
        )

        # 保存结果
        output_dir = Path("output")
        save_results(results, output_dir)

        console.print("\n[bold green]✅ 原型测试完成！[/bold green]")

    except Exception as e:
        console.print(f"\n[red]❌ 错误: {str(e)}[/red]")
        import traceback
        console.print(traceback.format_exc())


if __name__ == "__main__":
    main()
