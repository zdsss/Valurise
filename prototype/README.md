# Valurise MVP Prototype

AI驱动的职业价值发现引擎 - 技术原型

## 概述

这是Valurise的技术原型，用于验证多Agent架构在职业价值发现中的可行性和成本效益。

### 核心功能

**4个专业化Agent协作**：

1. **信息提取Agent** - 从用户输入中提取结构化信息
2. **价值分析Agent** - 深度挖掘职业价值，量化成就，识别可迁移技能
3. **叙事策略Agent** - 构建职业故事，制定定位策略
4. **简历格式化Agent** - 生成优化的简历，ATS友好

### 验证目标

- ✅ 多Agent架构的实际效果
- ✅ AI成本控制（目标：<$2/次）
- ✅ 价值发现的可行性
- ✅ 处理时间和用户体验

## 快速开始

### 1. 安装依赖

```bash
cd prototype
pip install -r requirements.txt
```

### 2. 配置API Key

复制`.env.example`为`.env`并填入你的Anthropic API key：

```bash
cp .env.example .env
```

编辑`.env`：
```
ANTHROPIC_API_KEY=your_actual_api_key_here
```

### 3. 运行原型

```bash
python main.py
```

## 项目结构

```
prototype/
├── models.py          # 数据模型定义
├── agents.py          # 4个Agent的实现
├── main.py            # CLI界面
├── requirements.txt   # 依赖
├── .env.example       # 环境变量模板
└── output/            # 输出结果（自动生成）
```

## 技术架构

### Agent工作流

```
用户输入
    ↓
[Agent 1: 信息提取]
    ↓
结构化用户档案
    ↓
[Agent 2: 价值分析]
    ↓
量化成就 + 可迁移技能 + 能力图谱
    ↓
[Agent 3: 叙事策略]
    ↓
职业故事 + 定位陈述 + 差异化点
    ↓
[Agent 4: 简历格式化]
    ↓
优化的简历版本
```

### 成本优化策略

1. **结构化输出** - 使用JSON Schema减少解析成本
2. **Prompt优化** - 精简system prompt，减少input tokens
3. **模型选择** - 核心分析用Sonnet，格式化可用Haiku
4. **批处理** - 非实时部分可异步处理

### 预期成本分解

基于Sonnet 4.6定价（$3/M input, $15/M output）：

| Agent | Input Tokens | Output Tokens | 成本 |
|-------|--------------|---------------|------|
| 信息提取 | ~2000 | ~1000 | $0.02 |
| 价值分析 | ~3000 | ~2000 | $0.04 |
| 叙事策略 | ~4000 | ~1500 | $0.03 |
| 简历格式化 | ~5000 | ~2000 | $0.05 |
| **总计** | ~14000 | ~6500 | **~$0.14** |

实际成本可能因用户输入长度而异，但应远低于$2目标。

## 示例输出

运行原型后，你将看到：

1. **信息提取结果** - 结构化的用户档案
2. **价值分析** - 量化的成就、可迁移技能、独特价值主张
3. **叙事策略** - 职业故事、定位陈述、差异化点
4. **简历版本** - 优化的简历内容
5. **成本分析** - 各Agent的成本和总成本

完整结果保存在`output/valurise_output.json`。

## 下一步

### 原型验证后的改进方向

1. **用户体验**
   - 对话式信息收集（而非一次性输入）
   - 交互式优化（用户可调整重点）
   - 可视化价值分析过程

2. **功能增强**
   - 多版本简历（针对不同岗位）
   - LinkedIn优化
   - 面试准备材料
   - 职业发展建议

3. **成本优化**
   - Prompt caching（Anthropic支持）
   - 混合模型（Sonnet + Haiku）
   - 增量更新（而非每次全量处理）

4. **质量提升**
   - 人工审核流程
   - 用户反馈循环
   - A/B测试不同prompt策略

## 技术栈

- **AI**: Anthropic Claude API (Sonnet 4.6)
- **语言**: Python 3.10+
- **数据验证**: Pydantic
- **CLI**: Rich, Typer
- **测试**: Pytest

## 许可

MIT License

## 联系

如有问题或建议，请联系项目团队。
