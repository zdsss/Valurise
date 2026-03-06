# Railway环境配置步骤指南

**日期**: 2026年3月6日
**方案**: Railway在线部署
**状态**: 🔄 进行中

---

## 📋 配置步骤

### 步骤1：注册Railway账号 ⏳

**操作**：
1. 访问 https://railway.app
2. 点击 "Start a New Project" 或 "Login"
3. 选择 "Login with GitHub"
4. 授权Railway访问GitHub
5. 验证邮箱（如需要）

**预计时间**: 2-3分钟

---

### 步骤2：创建新项目 ⏳

**操作**：
1. 登录后，点击 "New Project"
2. 选择 "Empty Project"
3. 项目会自动创建

**预计时间**: 30秒

---

### 步骤3：添加PostgreSQL数据库 ⏳

**操作**：
1. 在项目页面，点击 "+ New"
2. 选择 "Database"
3. 选择 "Add PostgreSQL"
4. 等待部署完成（会显示绿色✓）
5. 点击PostgreSQL服务卡片
6. 切换到 "Variables" 标签
7. 找到并复制 `DATABASE_URL` 的值

**DATABASE_URL格式**：
```
postgresql://postgres:密码@主机:端口/数据库名
```

**示例**：
```
postgresql://postgres:abc123xyz@containers-us-west-123.railway.app:5432/railway
```

**预计时间**: 2-3分钟

---

### 步骤4：添加Redis数据库 ⏳

**操作**：
1. 在项目页面，点击 "+ New"
2. 选择 "Database"
3. 选择 "Add Redis"
4. 等待部署完成（会显示绿色✓）
5. 点击Redis服务卡片
6. 切换到 "Variables" 标签
7. 找到并复制 `REDIS_URL` 的值

**REDIS_URL格式**：
```
redis://default:密码@主机:端口
```

**示例**：
```
redis://default:abc123xyz@containers-us-west-123.railway.app:6379
```

**预计时间**: 2-3分钟

---

### 步骤5：提供连接信息给我 ⏳

**需要提供**：
1. `DATABASE_URL` - PostgreSQL连接字符串
2. `REDIS_URL` - Redis连接字符串

**格式**：
```
DATABASE_URL=postgresql://postgres:xxx@xxx.railway.app:5432/railway
REDIS_URL=redis://default:xxx@xxx.railway.app:6379
```

**注意**：
- 这些URL包含密码，是敏感信息
- 只在私密环境中分享
- 不要提交到Git

---

### 步骤6：我来配置后端 ⏳

**我会做的事情**：
1. 更新 `backend/.env` 文件
2. 添加完整的环境变量配置
3. 生成JWT密钥
4. 配置CORS
5. 启动FastAPI服务
6. 测试数据库连接

**预计时间**: 5分钟

---

### 步骤7：启动后端服务 ⏳

**我会执行**：
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**预计时间**: 2分钟

---

### 步骤8：测试API端点 ⏳

**测试内容**：
1. 健康检查: GET /health
2. API文档: GET /docs
3. 用户注册: POST /api/v1/auth/register
4. 用户登录: POST /api/v1/auth/login

**预计时间**: 5分钟

---

### 步骤9：启动Celery Worker ⏳

**我会执行**：
```bash
cd backend
celery -A app.core.celery_app worker --loglevel=info
```

**预计时间**: 2分钟

---

### 步骤10：前后端联调测试 ⏳

**测试流程**：
1. 前端连接后端
2. 测试用户注册
3. 测试用户登录
4. 测试创建分析
5. 测试查看结果

**预计时间**: 10-15分钟

---

## 📊 进度追踪

- [ ] 步骤1: 注册Railway账号
- [ ] 步骤2: 创建新项目
- [ ] 步骤3: 添加PostgreSQL
- [ ] 步骤4: 添加Redis
- [ ] 步骤5: 提供连接信息
- [ ] 步骤6: 配置后端环境
- [ ] 步骤7: 启动后端服务
- [ ] 步骤8: 测试API端点
- [ ] 步骤9: 启动Celery Worker
- [ ] 步骤10: 前后端联调

---

## 🎯 当前状态

**等待你完成**：步骤1-5（注册Railway并获取连接URL）

**完成后告诉我**：
```
DATABASE_URL=你的PostgreSQL连接字符串
REDIS_URL=你的Redis连接字符串
```

**然后我会**：立即配置并启动后端服务

---

## 💡 提示

### Railway免费额度
- $5免费额度
- PostgreSQL: ~$5/月
- Redis: ~$5/月
- 总计: ~$10/月
- 免费额度可用1个月

### 如果遇到问题
1. **无法注册**：尝试使用GitHub账号
2. **找不到Database选项**：确保在项目内部
3. **部署失败**：等待1-2分钟后刷新
4. **找不到URL**：在Variables标签中查找

---

**准备好了吗？开始注册Railway吧！** 🚀
