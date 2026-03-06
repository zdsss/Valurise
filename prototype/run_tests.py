"""
测试用例运行器
批量运行5个测试用例并收集结果
"""

import os
import json
import time
from pathlib import Path
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import print as rprint

from models import TargetRole
from agents import ValuriseOrchestrator

console = Console()

# 测试用例定义
TEST_CASES = [
    {
        "id": "case1",
        "name": "职业转型者（工程师转产品）",
        "input": """我叫李明，目前是一名后端工程师，有4年开发经验，现在想转型做产品经理。

工作经历：
1. 2020-现在：字节跳动 - 高级后端工程师
   - 负责推荐系统后端开发，日均处理10亿+请求
   - 优化算法性能，将响应时间从200ms降低到50ms
   - 参与产品需求评审，提出多个被采纳的产品建议
   - 带领3名初级工程师，指导代码review和技术方案

2. 2018-2020：美团 - 后端工程师
   - 开发外卖配送系统核心模块
   - 参与系统重构，提升系统稳定性到99.99%
   - 与产品经理紧密合作，理解业务需求并转化为技术方案

教育：
- 2014-2018：清华大学 - 软件工程学士

技能：
- 编程语言：Java, Python, Go
- 技术栈：Spring Boot, MySQL, Redis, Kafka
- 产品思维：用户研究、数据分析、需求分析
- 工具：Figma（自学）、SQL、数据可视化

我想转型的原因：
- 在技术工作中发现自己更喜欢思考"为什么做"而不是"怎么做"
- 多次参与产品讨论，提出的建议被采纳并产生了业务价值
- 希望能更直接地影响用户体验和业务结果""",
        "target_role": TargetRole(
            title="产品经理（技术方向）",
            industry="互联网/科技",
            key_requirements=["技术背景", "产品思维", "跨职能协作", "数据分析"]
        )
    },
    {
        "id": "case2",
        "name": "高潜力专业人士（晋升管理层）",
        "input": """我叫王芳，现任某头部互联网公司的高级运营经理，有6年运营经验，现在希望晋升为运营总监。

工作经历：
1. 2021-现在：腾讯 - 高级运营经理
   - 负责微信视频号创作者运营，管理200+头部创作者
   - 策划并执行创作者激励计划，使创作者留存率提升40%
   - 带领8人运营团队，制定季度OKR并超额完成
   - 跨部门协调产品、市场、商业化团队，推动3个重点项目落地
   - 建立数据驱动的运营体系，使内容播放量增长300%

2. 2018-2021：快手 - 运营经理
   - 负责短视频内容运营，管理50+MCN机构
   - 策划多个爆款活动，单次活动参与用户超1000万
   - 搭建运营SOP，使团队效率提升50%
   - 获得年度最佳运营奖

教育：
- 2014-2018：复旦大学 - 市场营销学士
- 2023：长江商学院 - EMBA在读

技能：
- 运营策略、用户增长、数据分析、团队管理
- 工具：SQL、Python（数据分析）、Tableau
- 跨部门协作、项目管理、战略规划

成就：
- 2022年腾讯优秀员工
- 管理的创作者总粉丝量超5000万
- 主导的项目为公司创造年收入2000万+""",
        "target_role": TargetRole(
            title="运营总监",
            industry="互联网/内容平台",
            key_requirements=["战略思维", "团队管理", "跨部门协作", "业务影响力", "数据驱动"]
        )
    },
    {
        "id": "case3",
        "name": "应届毕业生",
        "input": """我叫陈晓，2024年6月刚从大学毕业，现在在找第一份正式工作，目标是数据分析师。

教育：
- 2020-2024：上海交通大学 - 统计学学士
  - GPA: 3.8/4.0，专业排名前10%
  - 核心课程：概率论、数理统计、机器学习、数据挖掘、Python编程
  - 毕业论文：基于机器学习的用户行为预测模型（评分A+）

实习经历：
1. 2023.6-2023.9：阿里巴巴 - 数据分析实习生
   - 负责淘宝用户行为数据分析，支持产品决策
   - 使用SQL和Python分析100万+用户数据，发现3个关键洞察
   - 搭建用户留存分析dashboard，被产品团队持续使用
   - 参与A/B测试设计和结果分析，帮助优化转化率提升15%

2. 2023.1-2023.5：某创业公司 - 数据分析实习生（远程）
   - 分析用户增长数据，识别关键增长驱动因素
   - 制作周报和月报，向CEO汇报数据洞察
   - 使用Python自动化数据处理流程，节省团队50%时间

项目经历：
1. 校园数据竞赛 - 天池大数据竞赛（Top 5%）
   - 使用机器学习预测用户购买行为
   - 团队leader，协调3人团队分工

2. 个人项目 - 豆瓣电影推荐系统
   - 爬取10万+电影数据，构建推荐算法
   - 项目在GitHub获得200+ stars

技能：
- 编程：Python（熟练）、SQL（熟练）、R（基础）
- 工具：Tableau、Excel、Jupyter Notebook
- 统计分析、机器学习、数据可视化
- 英语：CET-6（580分），可阅读英文技术文档

获奖：
- 国家奖学金（2022）
- 天池大数据竞赛Top 5%
- 校优秀毕业生""",
        "target_role": TargetRole(
            title="数据分析师",
            industry="互联网/科技",
            key_requirements=["数据分析", "Python/SQL", "统计学基础", "业务理解", "学习能力"]
        )
    },
    {
        "id": "case4",
        "name": "资深专家（10+年）",
        "input": """我叫刘建国，有12年的技术管理经验，现任某互联网公司技术总监，希望寻找CTO或VP of Engineering的机会。

工作经历：
1. 2019-现在：某独角兽公司（估值$2B+）- 技术总监
   - 管理80+人的技术团队（前端、后端、算法、测试、运维）
   - 主导公司核心交易系统重构，支撑日交易额从1亿增长到10亿
   - 建立技术中台架构，使新业务上线时间从3个月缩短到2周
   - 推动DevOps转型，系统稳定性从99.5%提升到99.95%
   - 制定技术战略和roadmap，支持公司从B轮到D轮的快速增长
   - 建立技术人才梯队，培养出5名技术经理和2名架构师
   - 年度技术预算管理：$5M+

2. 2015-2019：美团 - 高级技术经理
   - 管理30人团队，负责外卖配送系统
   - 主导系统架构升级，支撑订单量从日均100万到1000万
   - 推动微服务化改造，系统可用性提升到99.99%
   - 获得美团年度技术创新奖

3. 2012-2015：百度 - 技术Leader
   - 带领10人团队，负责搜索广告系统
   - 优化广告投放算法，使CTR提升25%，年收入增加$50M+
   - 参与百度技术委员会，制定技术规范

教育：
- 2008-2012：浙江大学 - 计算机科学硕士
- 2004-2008：浙江大学 - 计算机科学学士

技能：
- 技术管理、架构设计、团队建设、战略规划
- 技术栈：分布式系统、微服务、云原生、大数据
- 业务理解、跨部门协作、预算管理
- 英语流利，可作为工作语言

成就：
- 管理过最大团队规模：80人
- 支持业务从0到年收入$100M+
- 培养出多名技术管理者
- 多次在技术大会演讲（QCon、ArchSummit）
- 技术博客粉丝10万+""",
        "target_role": TargetRole(
            title="CTO / VP of Engineering",
            industry="互联网/科技",
            key_requirements=["战略思维", "大规模团队管理", "技术深度", "业务理解", "高管领导力"]
        )
    },
    {
        "id": "case5",
        "name": "跨行业转型者",
        "input": """我叫赵敏，在传统制造业做了7年的供应链管理，现在想转型到互联网做供应链产品经理或运营。

工作经历：
1. 2020-现在：某汽车制造企业（世界500强）- 供应链高级经理
   - 管理价值$200M+的供应链网络，覆盖200+供应商
   - 主导供应链数字化转型项目，使库存周转率提升30%
   - 建立供应商评估体系，降低采购成本15%（年节省$30M）
   - 带领12人团队，负责采购、物流、库存管理
   - 使用数据分析优化供应链决策，减少缺货率50%

2. 2017-2020：某电子制造公司 - 供应链专员→主管
   - 负责原材料采购和供应商管理
   - 优化物流路线，降低运输成本20%
   - 参与ERP系统实施，提升供应链透明度

教育：
- 2013-2017：同济大学 - 物流管理学士
- 2024：在线学习产品经理课程（人人都是产品经理）

技能：
- 供应链管理、采购、物流、库存优化
- 数据分析：Excel（高级）、SQL（自学中）、Power BI
- 项目管理、跨部门协作、供应商谈判
- 正在学习：产品思维、用户研究、敏捷开发

为什么转型：
- 在数字化转型项目中，发现自己对产品和技术更感兴趣
- 传统制造业节奏慢，希望在更快速迭代的环境中工作
- 看到电商和新零售对供应链的重塑，想参与其中
- 供应链经验在互联网公司（如电商、新零售）有很大价值

自我提升：
- 学习了产品经理课程，完成3个产品设计作业
- 研究了京东、美团、盒马的供应链产品
- 自学SQL和Python，能做基础数据分析
- 关注供应链科技领域的创业公司""",
        "target_role": TargetRole(
            title="供应链产品经理",
            industry="电商/新零售/物流科技",
            key_requirements=["供应链专业知识", "产品思维", "数据分析", "数字化经验", "学习能力"]
        )
    }
]


def run_test_case(orchestrator, test_case):
    """运行单个测试用例"""
    console.print(f"\n{'='*60}")
    console.print(f"[bold cyan]测试用例: {test_case['name']}[/bold cyan]")
    console.print(f"{'='*60}\n")

    start_time = time.time()

    try:
        results = orchestrator.process(
            raw_input=test_case['input'],
            target_role=test_case['target_role'],
            num_versions=1
        )

        duration = time.time() - start_time

        # 提取关键指标
        total_cost = results['total_cost']

        console.print(f"\n[green]✓ 测试完成[/green]")
        console.print(f"  成本: ${total_cost:.4f}")
        console.print(f"  时间: {duration:.1f}秒")

        return {
            "case_id": test_case['id'],
            "case_name": test_case['name'],
            "success": True,
            "cost": total_cost,
            "duration": duration,
            "results": results
        }

    except Exception as e:
        console.print(f"\n[red]✗ 测试失败: {e}[/red]")
        return {
            "case_id": test_case['id'],
            "case_name": test_case['name'],
            "success": False,
            "error": str(e)
        }


def main():
    """主函数"""
    console.print(Panel.fit(
        "[bold cyan]Valurise 测试用例批量运行器[/bold cyan]\n"
        "运行5个不同场景的测试用例",
        border_style="cyan"
    ))

    # 加载环境变量
    load_dotenv()
    api_key = os.getenv("ANTHROPIC_API_KEY")
    base_url = os.getenv("ANTHROPIC_BASE_URL")

    if not api_key:
        console.print("[red]错误: 未找到ANTHROPIC_API_KEY[/red]")
        return

    # 初始化Orchestrator
    console.print("\n[bold]初始化系统...[/bold]")
    orchestrator = ValuriseOrchestrator(
        api_key=api_key,
        model_main=os.getenv("MODEL_MAIN", "claude-sonnet-4-6"),
        base_url=base_url
    )

    # 运行所有测试用例
    results = []
    for test_case in TEST_CASES:
        result = run_test_case(orchestrator, test_case)
        results.append(result)

        # 保存单个测试结果
        output_dir = Path("test_results")
        output_dir.mkdir(exist_ok=True)

        output_file = output_dir / f"{result['case_id']}_result.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2, default=str)

        console.print(f"  结果已保存: {output_file}")

        # 短暂休息，避免API限流
        if test_case != TEST_CASES[-1]:
            console.print("\n[dim]等待5秒后继续下一个测试...[/dim]")
            time.sleep(5)

    # 生成汇总报告
    console.print(f"\n{'='*60}")
    console.print("[bold cyan]测试汇总报告[/bold cyan]")
    console.print(f"{'='*60}\n")

    # 统计数据
    successful_tests = [r for r in results if r['success']]
    failed_tests = [r for r in results if not r['success']]

    if successful_tests:
        costs = [r['cost'] for r in successful_tests]
        durations = [r['duration'] for r in successful_tests]

        avg_cost = sum(costs) / len(costs)
        max_cost = max(costs)
        min_cost = min(costs)

        avg_duration = sum(durations) / len(durations)

        # 成本表格
        table = Table(title="成本分析")
        table.add_column("指标", style="cyan")
        table.add_column("值", style="green")
        table.add_column("目标", style="yellow")
        table.add_column("状态", style="bold")

        table.add_row(
            "平均成本",
            f"${avg_cost:.4f}",
            "< $0.30",
            "✓" if avg_cost < 0.30 else "✗"
        )
        table.add_row(
            "最大成本",
            f"${max_cost:.4f}",
            "< $0.50",
            "✓" if max_cost < 0.50 else "✗"
        )
        table.add_row(
            "最小成本",
            f"${min_cost:.4f}",
            "-",
            "-"
        )
        table.add_row(
            "平均时间",
            f"{avg_duration:.1f}秒",
            "-",
            "-"
        )

        console.print(table)

        # 详细结果表格
        detail_table = Table(title="\n测试用例详情")
        detail_table.add_column("用例", style="cyan")
        detail_table.add_column("成本", style="green")
        detail_table.add_column("时间", style="yellow")
        detail_table.add_column("状态", style="bold")

        for r in results:
            if r['success']:
                detail_table.add_row(
                    r['case_name'],
                    f"${r['cost']:.4f}",
                    f"{r['duration']:.1f}s",
                    "✓"
                )
            else:
                detail_table.add_row(
                    r['case_name'],
                    "-",
                    "-",
                    f"✗ {r.get('error', 'Unknown error')}"
                )

        console.print(detail_table)

    # 保存汇总报告
    summary = {
        "total_tests": len(results),
        "successful": len(successful_tests),
        "failed": len(failed_tests),
        "avg_cost": avg_cost if successful_tests else 0,
        "max_cost": max_cost if successful_tests else 0,
        "min_cost": min_cost if successful_tests else 0,
        "avg_duration": avg_duration if successful_tests else 0,
        "results": results
    }

    summary_file = Path("test_results/summary.json")
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2, default=str)

    console.print(f"\n[bold green]汇总报告已保存: {summary_file}[/bold green]")

    # 结论
    if successful_tests:
        if avg_cost < 0.30 and max_cost < 0.50:
            console.print("\n[bold green]✓ 成本控制目标达成！[/bold green]")
        else:
            console.print("\n[bold yellow]⚠ 成本控制需要优化[/bold yellow]")


if __name__ == "__main__":
    main()
