"""
用户反馈数据收集和分析工具
自动计算满意度、付费意愿、NPS等关键指标
"""

import json
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()


def load_feedback_data():
    """加载用户反馈数据"""
    feedback_file = Path("user_feedback_data.json")

    if not feedback_file.exists():
        return {
            "users": [],
            "summary": {
                "total_users": 0,
                "avg_satisfaction": 0,
                "willing_to_pay_percentage": 0,
                "nps": 0
            }
        }

    with open(feedback_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def add_user_feedback():
    """添加新的用户反馈"""
    console.print(Panel.fit(
        "[bold cyan]添加用户反馈[/bold cyan]",
        border_style="cyan"
    ))

    # 基本信息
    console.print("\n[bold]基本信息[/bold]")
    user_name = input("用户姓名/昵称: ")
    background = input("职业背景: ")
    test_date = input("测试日期 (YYYY-MM-DD): ")

    # 输出质量评分
    console.print("\n[bold]输出质量评分 (1-5分)[/bold]")
    extraction_score = int(input("1. 信息提取准确性 (1-5): "))
    value_score = int(input("2. 价值分析深度 (1-5): "))
    narrative_score = int(input("3. 叙事策略说服力 (1-5): "))
    resume_score = int(input("4. 简历格式专业性 (1-5): "))

    # 整体满意度
    console.print("\n[bold]整体满意度[/bold]")
    overall_satisfaction = int(input("总体评分 (1-5): "))

    # 付费意愿
    console.print("\n[bold]付费意愿[/bold]")
    console.print("1. 是，我会付费使用")
    console.print("2. 可能会，取决于价格")
    console.print("3. 不确定")
    console.print("4. 可能不会")
    console.print("5. 不会付费")
    willing_to_pay = int(input("选择 (1-5): "))

    # 价格接受度
    console.print("\n[bold]价格接受度[/bold]")
    console.print("您认为合理的价格是多少？")
    console.print("1. $29以下")
    console.print("2. $49")
    console.print("3. $99")
    console.print("4. $199")
    console.print("5. $299以上")
    price_point = int(input("选择 (1-5): "))

    # NPS评分
    console.print("\n[bold]推荐意愿 (NPS)[/bold]")
    nps_score = int(input("您有多大可能向朋友推荐 (0-10): "))

    # 文字反馈
    console.print("\n[bold]文字反馈[/bold]")
    best_feature = input("最喜欢的功能/特点: ")
    improvement = input("最需要改进的地方: ")
    other_feedback = input("其他反馈: ")

    # 构建反馈数据
    feedback = {
        "user_name": user_name,
        "background": background,
        "test_date": test_date,
        "scores": {
            "extraction": extraction_score,
            "value_analysis": value_score,
            "narrative": narrative_score,
            "resume": resume_score,
            "overall": overall_satisfaction
        },
        "willing_to_pay": willing_to_pay,
        "price_point": price_point,
        "nps_score": nps_score,
        "feedback": {
            "best_feature": best_feature,
            "improvement": improvement,
            "other": other_feedback
        }
    }

    return feedback


def calculate_metrics(data):
    """计算关键指标"""
    if not data["users"]:
        return None

    users = data["users"]
    n = len(users)

    # 平均满意度
    avg_satisfaction = sum(u["scores"]["overall"] for u in users) / n

    # 付费意愿比例 (选择1或2的用户)
    willing_users = sum(1 for u in users if u["willing_to_pay"] <= 2)
    willing_percentage = (willing_users / n) * 100

    # 愿意支付$99的比例 (price_point >= 3)
    willing_99 = sum(1 for u in users if u["price_point"] >= 3)
    willing_99_percentage = (willing_99 / n) * 100

    # NPS计算
    promoters = sum(1 for u in users if u["nps_score"] >= 9)
    passives = sum(1 for u in users if 7 <= u["nps_score"] <= 8)
    detractors = sum(1 for u in users if u["nps_score"] <= 6)

    nps = ((promoters - detractors) / n) * 100

    # 各项评分平均值
    avg_extraction = sum(u["scores"]["extraction"] for u in users) / n
    avg_value = sum(u["scores"]["value_analysis"] for u in users) / n
    avg_narrative = sum(u["scores"]["narrative"] for u in users) / n
    avg_resume = sum(u["scores"]["resume"] for u in users) / n

    return {
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


def display_summary(metrics):
    """显示汇总数据"""
    if not metrics:
        console.print("[yellow]暂无用户反馈数据[/yellow]")
        return

    console.print("\n" + "="*60)
    console.print("[bold cyan]用户反馈汇总[/bold cyan]")
    console.print("="*60 + "\n")

    # Go/No-Go标准表格
    table = Table(title="Go/No-Go 决策标准")
    table.add_column("指标", style="cyan")
    table.add_column("当前值", style="green")
    table.add_column("目标值", style="yellow")
    table.add_column("状态", style="bold")

    # 用户数量
    table.add_row(
        "测试用户数",
        str(metrics["total_users"]),
        "5-10",
        "✓" if metrics["total_users"] >= 5 else "⏳"
    )

    # 平均满意度
    table.add_row(
        "平均满意度",
        f"{metrics['avg_satisfaction']:.2f}/5",
        "> 3.5/5",
        "✓" if metrics["avg_satisfaction"] > 3.5 else "✗"
    )

    # 付费意愿
    table.add_row(
        "付费意愿",
        f"{metrics['willing_to_pay_percentage']:.1f}%",
        "> 50%",
        "✓" if metrics["willing_to_pay_percentage"] > 50 else "✗"
    )

    # 愿意支付$99
    table.add_row(
        "愿意支付$99",
        f"{metrics['willing_99_percentage']:.1f}%",
        "> 50%",
        "✓" if metrics["willing_99_percentage"] > 50 else "✗"
    )

    # NPS
    table.add_row(
        "NPS评分",
        f"{metrics['nps']:.1f}",
        "> 30",
        "✓" if metrics["nps"] > 30 else "✗"
    )

    console.print(table)

    # NPS分解
    console.print(f"\n[bold]NPS分解:[/bold]")
    console.print(f"  推荐者 (9-10分): {metrics['nps_breakdown']['promoters']}人")
    console.print(f"  中立者 (7-8分): {metrics['nps_breakdown']['passives']}人")
    console.print(f"  贬损者 (0-6分): {metrics['nps_breakdown']['detractors']}人")

    # 各项评分
    console.print(f"\n[bold]各项评分平均值:[/bold]")
    scores = metrics['avg_scores']
    console.print(f"  信息提取: {scores['extraction']:.2f}/5")
    console.print(f"  价值分析: {scores['value_analysis']:.2f}/5")
    console.print(f"  叙事策略: {scores['narrative']:.2f}/5")
    console.print(f"  简历格式: {scores['resume']:.2f}/5")

    # Go/No-Go建议
    console.print(f"\n[bold]Go/No-Go 建议:[/bold]")

    go_criteria = [
        metrics["total_users"] >= 5,
        metrics["avg_satisfaction"] > 3.5,
        metrics["willing_99_percentage"] > 50,
        metrics["nps"] > 30
    ]

    if all(go_criteria):
        console.print("[bold green]✓ 建议 GO - 所有标准达成，可以进入Web开发阶段[/bold green]")
    elif sum(go_criteria) >= 3:
        console.print("[bold yellow]⚠ 建议 GO with caution - 大部分标准达成，但需要关注未达标项[/bold yellow]")
    else:
        console.print("[bold red]✗ 建议 NO-GO - 多项标准未达成，需要优化产品或重新测试[/bold red]")


def save_data(data):
    """保存数据"""
    with open("user_feedback_data.json", 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    console.print("\n[green]✓ 数据已保存[/green]")


def main():
    """主函数"""
    console.print(Panel.fit(
        "[bold cyan]Valurise 用户反馈收集工具[/bold cyan]\n"
        "收集和分析用户反馈数据",
        border_style="cyan"
    ))

    while True:
        console.print("\n[bold]选择操作:[/bold]")
        console.print("1. 添加新的用户反馈")
        console.print("2. 查看汇总数据")
        console.print("3. 查看所有用户反馈")
        console.print("4. 退出")

        choice = input("\n请选择 (1-4): ")

        if choice == "1":
            # 添加反馈
            feedback = add_user_feedback()

            # 加载现有数据
            data = load_feedback_data()
            data["users"].append(feedback)

            # 重新计算指标
            metrics = calculate_metrics(data)
            if metrics:
                data["summary"] = metrics

            # 保存
            save_data(data)

            console.print(f"\n[green]✓ 已添加用户 {feedback['user_name']} 的反馈[/green]")

        elif choice == "2":
            # 查看汇总
            data = load_feedback_data()
            metrics = calculate_metrics(data)
            display_summary(metrics)

        elif choice == "3":
            # 查看所有反馈
            data = load_feedback_data()
            if not data["users"]:
                console.print("[yellow]暂无用户反馈数据[/yellow]")
            else:
                console.print(f"\n[bold]共有 {len(data['users'])} 位用户的反馈:[/bold]\n")
                for i, user in enumerate(data["users"], 1):
                    console.print(f"{i}. {user['user_name']} ({user['background']}) - {user['test_date']}")
                    console.print(f"   满意度: {user['scores']['overall']}/5, NPS: {user['nps_score']}/10")
                    console.print(f"   最喜欢: {user['feedback']['best_feature']}")
                    console.print(f"   需改进: {user['feedback']['improvement']}\n")

        elif choice == "4":
            console.print("\n[cyan]再见！[/cyan]")
            break

        else:
            console.print("[red]无效选择，请重试[/red]")


if __name__ == "__main__":
    main()
