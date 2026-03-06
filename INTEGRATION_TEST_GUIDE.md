# Valurise 前后端联调测试指南

**日期**: 2026年3月6日
**阶段**: Week 3 Day 7
**目标**: 完成前后端联调测试，确保所有功能正常工作

---

## 测试环境准备

### 1. 后端服务启动

#### 1.1 启动PostgreSQL

**使用Docker（推荐）**:
```bash
docker run -d --name valurise-postgres \
  -e POSTGRES_DB=valurise \
  -e POSTGRES_USER=valurise \
  -e POSTGRES_PASSWORD=password \
  -p 5432:5432 \
  postgres:15
```

**或使用本地PostgreSQL**:
```bash
# 创建数据库
createdb valurise

# 配置环境变量
export DATABASE_URL="postgresql://valurise:password@localhost:5432/valurise"
```

#### 1.2 启动Redis

**使用Docker（推荐）**:
```bash
docker run -d --name valurise-redis \
  -p 6379:6379 \
  redis:7
```

**或使用本地Redis**:
```bash
redis-server
```

#### 1.3 配置环境变量

编辑 `backend/.env`:
```bash
# 数据库配置
DATABASE_URL=postgresql://valurise:password@localhost:5432/valurise

# Redis配置
REDIS_URL=redis://localhost:6379/0

# JWT配置
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Anthropic API
ANTHROPIC_API_KEY=your-anthropic-api-key

# Stripe配置（测试模式）
STRIPE_SECRET_KEY=sk_test_your_stripe_test_key
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret
```

#### 1.4 启动FastAPI服务

```bash
cd backend
chmod +x start.sh
./start.sh
```

访问 http://localhost:8000/docs 查看API文档

#### 1.5 启动Celery Worker

**新开一个终端**:
```bash
cd backend
chmod +x start_worker.sh
./start_worker.sh
```

### 2. 前端服务启动

```bash
cd frontend

# 配置环境变量
echo "VITE_API_URL=http://localhost:8000/api/v1" > .env

# 启动开发服务器
npm run dev
```

访问 http://localhost:5173

---

## 测试用例

### 测试1: 用户注册和登录

#### 1.1 注册新用户

**步骤**:
1. 访问 http://localhost:5173/register
2. 填写表单:
   - 姓名: 测试用户
   - 邮箱: test@example.com
   - 密码: password123
   - 确认密码: password123
3. 点击"注册"

**预期结果**:
- ✅ 注册成功
- ✅ 自动登录
- ✅ 跳转到Dashboard
- ✅ 显示用户信息

**验证API**:
```bash
# 查看数据库
psql valurise -c "SELECT id, email, full_name, created_at FROM users;"
```

#### 1.2 登出和登录

**步骤**:
1. 点击右上角"退出"
2. 跳转到首页
3. 点击"登录"
4. 输入邮箱和密码
5. 点击"登录"

**预期结果**:
- ✅ 登出成功
- ✅ 登录成功
- ✅ 跳转到Dashboard
- ✅ Token保存到localStorage

**验证Token**:
```javascript
// 在浏览器控制台执行
console.log(localStorage.getItem('access_token'));
```

---

### 测试2: 创建职业分析

#### 2.1 填写职业信息

**步骤**:
1. 在Dashboard点击"开始新分析"
2. 填写职业经历（至少100字）:
```
我在过去5年担任产品经理，主导了3个从0到1的产品项目。

项目A：用户增长从0到50万，月活跃率达到65%
- 负责产品规划和需求分析
- 带领8人团队完成产品开发
- 通过数据分析优化用户体验

项目B：B2B SaaS产品，年收入达到500万
- 从市场调研到产品上线全流程负责
- 建立了完整的客户成功体系
- 客户续费率达到85%

核心技能：
- 用户研究和需求分析
- 数据驱动决策
- 敏捷开发管理
- 跨部门协作
```

3. 填写目标岗位: "高级产品经理"
4. 填写目标行业: "互联网"
5. 点击"开始分析"

**预期结果**:
- ✅ 表单验证通过
- ✅ 提交成功
- ✅ 跳转到进度页面

#### 2.2 查看分析进度

**预期结果**:
- ✅ 显示当前步骤
- ✅ 进度条更新
- ✅ 每3秒轮询一次
- ✅ 显示4个Agent的状态:
  - 📋 提取职业信息
  - 💎 分析职业价值
  - 📖 构建叙事策略
  - ✨ 优化简历

**验证后端**:
```bash
# 查看Celery日志
tail -f backend/celery.log

# 查看分析状态
curl http://localhost:8000/api/v1/analyses/{analysis_id} \
  -H "Authorization: Bearer YOUR_TOKEN"
```

#### 2.3 查看分析结果

**预期结果**:
- ✅ 分析完成后自动跳转
- ✅ 显示4个标签页:
  1. **职业信息**: 工作经历、技能、成就
  2. **价值分析**: 价值主张、可迁移技能、量化成果
  3. **叙事策略**: 职业故事、故事弧线、定位陈述
  4. **优化简历**: 简历摘要、工作经历、ATS关键词
- ✅ 显示统计信息（时间、成本、Token）
- ✅ 可以打印报告

**验证数据**:
```bash
# 查看数据库
psql valurise -c "SELECT id, status, created_at, completed_at FROM analyses ORDER BY created_at DESC LIMIT 1;"
```

---

### 测试3: Dashboard功能

#### 3.1 查看分析历史

**步骤**:
1. 返回Dashboard
2. 查看"我的分析"列表

**预期结果**:
- ✅ 显示所有分析记录
- ✅ 显示状态标签（等待中/处理中/已完成/失败）
- ✅ 显示创建时间和完成时间
- ✅ 可以点击"查看结果"

#### 3.2 查看统计信息

**预期结果**:
- ✅ 显示已完成分析数量
- ✅ 显示剩余积分
- ✅ 显示用户信息

---

### 测试4: 定价和支付（可选）

**注意**: 需要配置Stripe测试密钥

#### 4.1 查看定价页面

**步骤**:
1. 点击导航栏"定价"
2. 查看3个定价方案

**预期结果**:
- ✅ 显示基础版（$49）
- ✅ 显示专业版（$99，推荐）
- ✅ 显示高级版（$199）
- ✅ 显示功能对比

#### 4.2 创建支付会话（测试模式）

**步骤**:
1. 点击"选择方案"
2. 跳转到Stripe Checkout

**预期结果**:
- ✅ 创建Checkout会话成功
- ✅ 跳转到Stripe支付页面

**测试支付**:
使用Stripe测试卡号:
- 卡号: 4242 4242 4242 4242
- 过期日期: 任意未来日期
- CVC: 任意3位数字

#### 4.3 支付成功

**预期结果**:
- ✅ 支付成功后跳转到成功页面
- ✅ 显示成功消息
- ✅ 可以开始新分析

---

## 常见问题排查

### 问题1: 后端启动失败

**检查**:
```bash
# 检查PostgreSQL连接
psql -h localhost -U valurise -d valurise

# 检查Redis连接
redis-cli ping

# 查看后端日志
tail -f backend/logs/app.log
```

### 问题2: 前端无法连接后端

**检查**:
```bash
# 测试API连接
curl http://localhost:8000/api/v1/health

# 检查CORS配置
# backend/app/main.py 中应该有:
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 问题3: Celery任务不执行

**检查**:
```bash
# 查看Celery Worker日志
tail -f backend/celery.log

# 检查Redis连接
redis-cli
> KEYS *

# 手动测试任务
python -c "from app.tasks import process_analysis; process_analysis.delay('test-id')"
```

### 问题4: 分析失败

**检查**:
```bash
# 查看错误信息
psql valurise -c "SELECT id, status, error_message FROM analyses WHERE status='failed';"

# 检查Anthropic API Key
echo $ANTHROPIC_API_KEY

# 测试Agent
cd backend
python test_optimized_agents.py
```

---

## 性能测试

### 1. 分析处理时间

**目标**: < 4分钟

**测试**:
```bash
# 记录开始时间
start_time=$(date +%s)

# 创建分析（通过API或前端）

# 等待完成，记录结束时间
end_time=$(date +%s)
echo "处理时间: $((end_time - start_time)) 秒"
```

### 2. API响应时间

**目标**: < 200ms

**测试**:
```bash
# 测试登录API
time curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'

# 测试获取用户信息
time curl http://localhost:8000/api/v1/users/me \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 3. 前端加载时间

**测试**:
1. 打开浏览器开发者工具
2. 切换到Network标签
3. 刷新页面
4. 查看DOMContentLoaded和Load时间

**目标**:
- DOMContentLoaded: < 1秒
- Load: < 3秒

---

## 测试检查清单

### 后端测试
- [ ] PostgreSQL连接正常
- [ ] Redis连接正常
- [ ] FastAPI服务启动成功
- [ ] Celery Worker运行正常
- [ ] API文档可访问（/docs）
- [ ] 健康检查通过（/health）

### 前端测试
- [ ] 开发服务器启动成功
- [ ] 首页正常显示
- [ ] 路由跳转正常
- [ ] 样式渲染正确
- [ ] 无控制台错误

### 功能测试
- [ ] 用户注册成功
- [ ] 用户登录成功
- [ ] Token管理正常
- [ ] 创建分析成功
- [ ] 进度显示正常
- [ ] 结果展示完整
- [ ] Dashboard功能正常
- [ ] 定价页面正常
- [ ] 支付流程正常（可选）

### 错误处理
- [ ] 网络错误提示
- [ ] 表单验证错误
- [ ] API错误提示
- [ ] 401自动跳转登录
- [ ] 404页面处理

---

## 测试报告模板

```markdown
# Valurise 联调测试报告

**测试日期**: 2026年3月6日
**测试人员**: [姓名]
**测试环境**:
- 后端: FastAPI + PostgreSQL + Redis + Celery
- 前端: React + Vite

## 测试结果

### 1. 用户认证
- 注册: ✅ 通过 / ❌ 失败
- 登录: ✅ 通过 / ❌ 失败
- 登出: ✅ 通过 / ❌ 失败

### 2. 分析流程
- 创建分析: ✅ 通过 / ❌ 失败
- 进度显示: ✅ 通过 / ❌ 失败
- 结果展示: ✅ 通过 / ❌ 失败

### 3. Dashboard
- 历史记录: ✅ 通过 / ❌ 失败
- 统计信息: ✅ 通过 / ❌ 失败

### 4. 支付集成
- 定价页面: ✅ 通过 / ❌ 失败
- 支付流程: ✅ 通过 / ❌ 失败

## 发现的问题

1. [问题描述]
   - 严重程度: 高/中/低
   - 复现步骤: ...
   - 预期结果: ...
   - 实际结果: ...

## 性能数据

- 分析处理时间: [X] 分钟
- API平均响应时间: [X] ms
- 前端加载时间: [X] 秒

## 总体评价

[总体评价和建议]
```

---

## 下一步

测试完成后：

1. **修复Bug**: 根据测试报告修复发现的问题
2. **性能优化**: 如果性能不达标，进行优化
3. **文档更新**: 更新README和部署文档
4. **准备部署**: 进入Week 4部署阶段

---

**祝测试顺利！** 🚀
