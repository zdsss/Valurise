# 🚀 Valurise Week 2-4 Web开发计划

**阶段**: Web MVP开发
**时间**: 2026年3月11日 - 4月1日（3周）
**目标**: 完成可运行的Web应用，准备Beta发布

---

## 📋 开发目标

### 核心目标

1. **功能完整**: 实现完整的用户流程（输入→处理→结果）
2. **用户体验**: 流畅的交互，清晰的进度提示
3. **支付集成**: Stripe支付，支持3个定价层级
4. **性能优化**: 处理时间<2分钟，异步处理
5. **部署上线**: 生产环境可访问

### 成功标准

- [ ] 用户可以完整走完流程
- [ ] 支付功能正常工作
- [ ] 处理时间<2分钟
- [ ] 移动端适配良好
- [ ] 通过10-15个内部用户测试

---

## 🏗️ 技术架构

### 技术栈选择

**前端**:
- **框架**: React 18 + TypeScript
- **构建工具**: Vite
- **样式**: TailwindCSS + shadcn/ui
- **状态管理**: Zustand（轻量级）
- **表单**: React Hook Form + Zod
- **HTTP**: Axios
- **部署**: Vercel

**后端**:
- **框架**: FastAPI (Python)
- **数据库**: PostgreSQL + SQLAlchemy
- **认证**: JWT + bcrypt
- **支付**: Stripe SDK
- **任务队列**: Celery + Redis（异步处理）
- **部署**: Railway / Render

**AI服务**:
- **API**: Anthropic Claude API
- **优化**: Prompt caching, 重试机制
- **监控**: 成本追踪，错误日志

### 系统架构图

```
┌─────────────┐
│   用户浏览器  │
└──────┬──────┘
       │
       ↓
┌─────────────────────────────┐
│  前端 (React + Vercel)       │
│  - 用户输入表单              │
│  - 进度展示                  │
│  - 结果展示                  │
│  - 支付流程                  │
└──────┬──────────────────────┘
       │ HTTPS/REST API
       ↓
┌─────────────────────────────┐
│  后端 (FastAPI + Railway)    │
│  - API路由                   │
│  - 用户认证                  │
│  - 订单管理                  │
│  - Webhook处理               │
└──────┬──────────────────────┘
       │
       ├─→ PostgreSQL (数据存储)
       │
       ├─→ Redis (任务队列)
       │   └─→ Celery Worker
       │       └─→ Anthropic API
       │           (4个Agent处理)
       │
       └─→ Stripe (支付处理)
```

---

## 📅 开发时间表

### Week 2 (3月11-17日): 技术优化 + 后端基础

**Day 1-2 (3月11-12日): 技术优化**
- [ ] 优化Agent代码（添加重试机制）
- [ ] 实现prompt caching
- [ ] 优化处理时间（目标<2分钟）
- [ ] 添加错误处理和日志

**Day 3-4 (3月13-14日): 后端基础**
- [ ] 初始化FastAPI项目
- [ ] 设置PostgreSQL数据库
- [ ] 实现用户模型和认证
- [ ] 实现订单模型

**Day 5-7 (3月15-17日): 核心API**
- [ ] 实现用户注册/登录API
- [ ] 实现分析任务API（异步）
- [ ] 集成Celery + Redis
- [ ] 集成4个Agent

**交付物**: 可运行的后端API

---

### Week 3 (3月18-24日): 前端开发 + 支付集成

**Day 1-2 (3月18-19日): 前端基础**
- [ ] 初始化React + Vite项目
- [ ] 设置TailwindCSS + shadcn/ui
- [ ] 实现路由结构
- [ ] 实现基础布局

**Day 3-4 (3月20-21日): 核心页面**
- [ ] 实现登录/注册页面
- [ ] 实现用户输入表单（多步骤）
- [ ] 实现进度展示页面
- [ ] 实现结果展示页面

**Day 5-6 (3月22-23日): 支付集成**
- [ ] 集成Stripe Checkout
- [ ] 实现定价页面
- [ ] 实现支付成功/失败页面
- [ ] 实现Webhook处理

**Day 7 (3月24日): 联调测试**
- [ ] 前后端联调
- [ ] 修复bug
- [ ] 性能优化

**交付物**: 完整的前端应用

---

### Week 4 (3月25-31日): 完善 + 测试 + 部署

**Day 1-2 (3月25-26日): 功能完善**
- [ ] 实现用户dashboard
- [ ] 实现历史记录查看
- [ ] 实现结果下载（PDF）
- [ ] 添加帮助文档

**Day 3-4 (3月27-28日): 部署上线**
- [ ] 部署后端到Railway
- [ ] 部署前端到Vercel
- [ ] 配置域名和SSL
- [ ] 设置监控和日志

**Day 5-7 (3月29-31日): 内部测试**
- [ ] 招募10-15个内部测试用户
- [ ] 收集反馈
- [ ] 修复bug
- [ ] 优化体验

**交付物**: 生产环境可用的Web应用

---

## 💻 详细开发任务

### 后端开发任务

#### 1. 项目初始化
```bash
# 创建项目结构
mkdir valurise-backend
cd valurise-backend
python -m venv venv
source venv/bin/activate
pip install fastapi uvicorn sqlalchemy psycopg2-binary pydantic-settings
pip install python-jose[cryptography] passlib[bcrypt]
pip install stripe celery redis anthropic
```

#### 2. 数据库模型

**User模型**:
```python
class User(Base):
    id: UUID
    email: str (unique)
    hashed_password: str
    created_at: datetime
    subscription_tier: str (basic/pro/premium)
```

**Analysis模型**:
```python
class Analysis(Base):
    id: UUID
    user_id: UUID (FK)
    status: str (pending/processing/completed/failed)
    input_data: JSON
    result_data: JSON
    cost: float
    created_at: datetime
    completed_at: datetime
```

**Order模型**:
```python
class Order(Base):
    id: UUID
    user_id: UUID (FK)
    analysis_id: UUID (FK)
    stripe_payment_id: str
    amount: int
    status: str (pending/paid/failed)
    created_at: datetime
```

#### 3. API端点

**认证相关**:
- `POST /api/auth/register` - 用户注册
- `POST /api/auth/login` - 用户登录
- `POST /api/auth/refresh` - 刷新token

**分析相关**:
- `POST /api/analysis/create` - 创建分析任务
- `GET /api/analysis/{id}` - 获取分析状态
- `GET /api/analysis/{id}/result` - 获取分析结果
- `GET /api/analysis/history` - 获取历史记录

**支付相关**:
- `POST /api/payment/create-checkout` - 创建支付会话
- `POST /api/payment/webhook` - Stripe webhook
- `GET /api/payment/verify/{session_id}` - 验证支付

#### 4. Celery任务

**分析任务**:
```python
@celery_app.task
def process_analysis(analysis_id: str):
    # 1. 获取分析记录
    # 2. 调用4个Agent
    # 3. 保存结果
    # 4. 更新状态
    # 5. 发送通知（可选）
```

---

### 前端开发任务

#### 1. 项目初始化
```bash
# 创建项目
npm create vite@latest valurise-frontend -- --template react-ts
cd valurise-frontend
npm install

# 安装依赖
npm install tailwindcss postcss autoprefixer
npm install @radix-ui/react-* # shadcn/ui组件
npm install react-router-dom axios zustand
npm install react-hook-form zod @hookform/resolvers
npm install @stripe/stripe-js @stripe/react-stripe-js
```

#### 2. 页面结构

```
/                       # 首页（Landing Page）
/login                  # 登录
/register               # 注册
/pricing                # 定价页面
/dashboard              # 用户dashboard
/analysis/new           # 新建分析
  /analysis/new/step1   # 基本信息
  /analysis/new/step2   # 工作经历
  /analysis/new/step3   # 教育背景
  /analysis/new/step4   # 目标岗位
/analysis/{id}/processing  # 处理中
/analysis/{id}/result      # 结果展示
/payment/checkout       # 支付页面
/payment/success        # 支付成功
/payment/cancel         # 支付取消
```

#### 3. 核心组件

**输入表单组件**:
- `BasicInfoForm` - 基本信息
- `WorkExperienceForm` - 工作经历（可添加多个）
- `EducationForm` - 教育背景
- `TargetRoleForm` - 目标岗位

**展示组件**:
- `ProcessingProgress` - 处理进度（4个Agent状态）
- `ValueAnalysisCard` - 价值分析展示
- `NarrativeCard` - 叙事策略展示
- `ResumePreview` - 简历预览
- `DownloadButton` - 下载按钮（PDF）

**支付组件**:
- `PricingCard` - 定价卡片
- `CheckoutForm` - 支付表单
- `PaymentStatus` - 支付状态

#### 4. 状态管理

```typescript
// useAuthStore
interface AuthState {
  user: User | null;
  token: string | null;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
}

// useAnalysisStore
interface AnalysisState {
  currentAnalysis: Analysis | null;
  history: Analysis[];
  createAnalysis: (data: AnalysisInput) => Promise<string>;
  fetchAnalysis: (id: string) => Promise<void>;
  fetchHistory: () => Promise<void>;
}
```

---

## 💰 支付集成方案

### Stripe集成

**定价配置**:
```typescript
const PRICING = {
  basic: {
    name: "基础版",
    price: 49,
    priceId: "price_xxx", // Stripe Price ID
    features: [
      "1次完整分析",
      "基础简历优化",
      "价值分析报告",
      "PDF下载"
    ]
  },
  pro: {
    name: "专业版",
    price: 99,
    priceId: "price_yyy",
    features: [
      "1次完整分析",
      "3个简历版本",
      "深度价值分析",
      "职业叙事策略",
      "PDF + Word下载",
      "优先支持"
    ]
  },
  premium: {
    name: "高级版",
    price: 199,
    priceId: "price_zzz",
    features: [
      "2次完整分析",
      "5个简历版本",
      "LinkedIn优化",
      "1次人工审核",
      "所有格式下载",
      "VIP支持"
    ]
  }
};
```

**支付流程**:
1. 用户选择定价层级
2. 前端调用 `POST /api/payment/create-checkout`
3. 后端创建Stripe Checkout Session
4. 前端重定向到Stripe支付页面
5. 用户完成支付
6. Stripe发送webhook到后端
7. 后端验证支付，创建分析任务
8. 前端重定向到处理页面

---

## 🎨 UI/UX设计要点

### 设计原则

1. **简洁清晰**: 减少认知负担，流程一目了然
2. **进度可见**: 实时显示处理进度，减少焦虑
3. **价值突出**: 清晰展示产品价值和差异化
4. **移动优先**: 响应式设计，移动端体验良好

### 关键页面设计

**Landing Page**:
- Hero区域：清晰的价值主张
- 功能展示：4个Agent的价值
- 案例展示：用户见证
- 定价对比：3个层级
- CTA按钮：开始使用

**输入表单**:
- 多步骤表单（4步）
- 进度指示器
- 自动保存
- 友好的错误提示

**处理页面**:
- 4个Agent的实时状态
- 预估剩余时间
- 有趣的等待动画
- 可以离开页面（邮件通知）

**结果页面**:
- 标签页切换（价值分析/叙事策略/简历）
- 可视化图表
- 高亮关键信息
- 一键下载

---

## 🔧 技术优化

### 1. 处理时间优化

**目标**: 从3.8分钟降到<2分钟

**优化策略**:
- **并行调用**: 部分Agent可以并行处理
- **Prompt caching**: 减少重复token
- **流式输出**: 边生成边展示（用户感知更快）
- **预加载**: 提前加载常用数据

**实现**:
```python
# 并行调用示例
async def process_analysis_optimized(input_data):
    # Step 1: 信息提取（必须先完成）
    extracted = await extraction_agent.extract(input_data)

    # Step 2-3: 价值分析和叙事策略可以并行
    value_task = asyncio.create_task(
        value_agent.analyze(extracted)
    )
    narrative_task = asyncio.create_task(
        narrative_agent.create(extracted)
    )

    value, narrative = await asyncio.gather(
        value_task, narrative_task
    )

    # Step 4: 简历格式化（依赖前面的结果）
    resume = await formatting_agent.format(
        extracted, value, narrative
    )

    return {
        "extracted": extracted,
        "value": value,
        "narrative": narrative,
        "resume": resume
    }
```

### 2. 成本优化

**目标**: 保持在$0.20以内

**优化策略**:
- **Prompt caching**: Anthropic支持，可节省50%+
- **混合模型**: 简单任务用Haiku（便宜5倍）
- **批处理**: 非实时任务批量处理
- **缓存结果**: 相似输入复用结果

### 3. 错误处理

**重试机制**:
```python
@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10),
    retry=retry_if_exception_type(APIError)
)
async def call_claude_with_retry(prompt):
    return await client.messages.create(...)
```

**降级策略**:
- API失败 → 重试3次
- 仍失败 → 使用备用模型
- 仍失败 → 返回部分结果 + 退款

---

## 📊 监控和分析

### 关键指标

**技术指标**:
- API响应时间
- 处理成功率
- 平均成本
- 错误率

**业务指标**:
- 注册转化率
- 支付转化率
- 用户满意度
- NPS评分

**工具**:
- **后端**: Sentry（错误监控）
- **前端**: Google Analytics
- **支付**: Stripe Dashboard
- **成本**: 自定义dashboard

---

## 🧪 测试计划

### Week 4 内部测试

**测试目标**: 10-15个内部用户

**测试重点**:
1. **功能测试**: 所有流程是否正常
2. **性能测试**: 处理时间是否<2分钟
3. **支付测试**: 支付流程是否顺畅
4. **体验测试**: 用户体验是否良好
5. **移动端测试**: 移动端是否正常

**测试流程**:
1. 发送测试邀请（提供测试账号）
2. 用户完整走一遍流程
3. 填写反馈问卷
4. 收集bug和改进建议
5. 快速迭代修复

**成功标准**:
- [ ] 功能完整性 > 95%
- [ ] 平均处理时间 < 2分钟
- [ ] 用户满意度 > 4.0/5
- [ ] 无重大bug
- [ ] 移动端体验良好

---

## 🚀 部署方案

### 后端部署（Railway）

**步骤**:
1. 创建Railway项目
2. 连接GitHub仓库
3. 添加PostgreSQL服务
4. 添加Redis服务
5. 配置环境变量
6. 自动部署

**环境变量**:
```
DATABASE_URL=postgresql://...
REDIS_URL=redis://...
ANTHROPIC_API_KEY=sk-...
STRIPE_SECRET_KEY=sk_...
STRIPE_WEBHOOK_SECRET=whsec_...
JWT_SECRET=...
```

### 前端部署（Vercel）

**步骤**:
1. 连接GitHub仓库
2. 配置构建命令
3. 配置环境变量
4. 自动部署

**环境变量**:
```
VITE_API_URL=https://api.valurise.com
VITE_STRIPE_PUBLIC_KEY=pk_...
```

### 域名配置

- 前端: `app.valurise.com`
- 后端: `api.valurise.com`
- SSL: 自动配置（Vercel/Railway提供）

---

## 📋 检查清单

### Week 2 完成标准
- [ ] Agent代码优化完成
- [ ] 后端API开发完成
- [ ] 数据库模型设计完成
- [ ] Celery任务队列配置完成
- [ ] API文档完成

### Week 3 完成标准
- [ ] 前端页面开发完成
- [ ] Stripe支付集成完成
- [ ] 前后端联调完成
- [ ] 基础功能测试通过

### Week 4 完成标准
- [ ] 部署到生产环境
- [ ] 10-15个内部用户测试完成
- [ ] 主要bug修复完成
- [ ] 准备Beta发布

---

## 💡 风险和应对

### 技术风险

**风险1**: 处理时间优化不达标
- **应对**: 降低目标到2.5分钟，继续优化

**风险2**: Stripe集成复杂
- **应对**: 使用Stripe Checkout（简化版），后续再优化

**风险3**: 部署问题
- **应对**: 提前1周部署测试环境

### 时间风险

**风险4**: 开发时间不足
- **应对**: 砍掉非核心功能（如LinkedIn优化）

**风险5**: 测试时间不足
- **应对**: 边开发边测试，滚动发布

---

## 📞 资源需求

### 人力资源

**理想配置**:
- 全栈开发 × 1（你）
- 前端开发 × 1（可选）
- 测试用户 × 10-15

**最小配置**:
- 全栈开发 × 1（你）
- 测试用户 × 10

### 技术资源

**必需**:
- Anthropic API账号
- Stripe账号
- Railway/Render账号
- Vercel账号
- 域名（可选）

**成本预估**:
- 开发环境: $0（本地）
- 生产环境: ~$50/月（Railway + Vercel）
- API成本: ~$20（测试阶段）
- 域名: ~$15/年（可选）

**总计**: ~$85（首月）

---

## 🎯 成功标准

### 技术标准
- [ ] 所有核心功能正常工作
- [ ] 处理时间 < 2分钟
- [ ] API成功率 > 99%
- [ ] 移动端适配良好

### 用户标准
- [ ] 10-15个内部用户测试完成
- [ ] 平均满意度 > 4.0/5
- [ ] 无重大用户体验问题
- [ ] 支付流程顺畅

### 业务标准
- [ ] 准备好Beta发布
- [ ] 营销材料准备完成
- [ ] 客服流程建立

---

**计划制定时间**: 2026年3月10日
**计划执行时间**: 2026年3月11日 - 4月1日
**下次复盘**: 2026年4月1日
