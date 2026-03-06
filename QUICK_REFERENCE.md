# Valurise 快速参考指南

**版本**: 1.0
**更新**: 2026年3月6日

---

## 🚀 快速启动

### 方式1: 使用启动脚本（推荐）

```bash
# 一键启动所有服务
chmod +x start_all.sh
./start_all.sh

# 停止所有服务
chmod +x stop_all.sh
./stop_all.sh
```

### 方式2: 手动启动

#### 1. 启动数据库服务

```bash
# PostgreSQL
docker run -d --name valurise-postgres \
  -e POSTGRES_DB=valurise \
  -e POSTGRES_USER=valurise \
  -e POSTGRES_PASSWORD=password \
  -p 5432:5432 postgres:15

# Redis
docker run -d --name valurise-redis \
  -p 6379:6379 redis:7
```

#### 2. 启动后端

```bash
cd backend
./start.sh              # FastAPI
./start_worker.sh       # Celery Worker（新终端）
```

#### 3. 启动前端

```bash
cd frontend
npm run dev
```

---

## 📍 访问地址

| 服务 | 地址 | 说明 |
|------|------|------|
| 前端应用 | http://localhost:5173 | React应用 |
| 后端API | http://localhost:8000 | FastAPI服务 |
| API文档 | http://localhost:8000/docs | Swagger UI |
| PostgreSQL | localhost:5432 | 数据库 |
| Redis | localhost:6379 | 缓存/队列 |

---

## 📁 项目结构

```
Valurise/
├── backend/                 # 后端服务
│   ├── app/                # FastAPI应用
│   ├── agents_optimized.py # AI Agents
│   ├── start.sh            # 启动脚本
│   └── requirements.txt    # Python依赖
│
├── frontend/               # 前端应用
│   ├── src/               # 源代码
│   ├── package.json       # Node依赖
│   └── README.md          # 前端文档
│
├── 项目文档/               # 项目文档
│   ├── WEEK1_COMPLETION.md
│   ├── WEEK2_COMPLETION_REPORT.md
│   ├── WEEK3_COMPLETION_REPORT.md
│   └── ...
│
├── INTEGRATION_TEST_GUIDE.md  # 测试指南
├── start_all.sh               # 快速启动
├── stop_all.sh                # 停止服务
└── README.md                  # 项目总览
```

---

## 🔑 环境变量

### 后端 (backend/.env)

```bash
# 数据库
DATABASE_URL=postgresql://valurise:password@localhost:5432/valurise

# Redis
REDIS_URL=redis://localhost:6379/0

# JWT
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Anthropic API
ANTHROPIC_API_KEY=your-anthropic-api-key

# Stripe
STRIPE_SECRET_KEY=sk_test_your_stripe_test_key
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret
```

### 前端 (frontend/.env)

```bash
VITE_API_URL=http://localhost:8000/api/v1
```

---

## 🧪 测试

### 运行测试

```bash
# 后端测试
cd backend
python test_optimized_agents.py

# 前端构建测试
cd frontend
npm run build
```

### 联调测试

参考 `INTEGRATION_TEST_GUIDE.md` 进行完整的联调测试。

---

## 📊 API端点

### 认证
- `POST /api/v1/auth/register` - 注册
- `POST /api/v1/auth/login` - 登录
- `POST /api/v1/auth/refresh` - 刷新Token

### 用户
- `GET /api/v1/users/me` - 获取当前用户
- `PATCH /api/v1/users/me` - 更新用户信息

### 分析
- `POST /api/v1/analyses` - 创建分析
- `GET /api/v1/analyses/{id}` - 获取分析状态
- `GET /api/v1/analyses/{id}/result` - 获取分析结果
- `GET /api/v1/analyses` - 获取分析历史

### 支付
- `POST /api/v1/payment/create-checkout` - 创建支付会话
- `GET /api/v1/payment/verify/{session_id}` - 验证支付

---

## 🐛 常见问题

### 1. 后端启动失败

**问题**: `ModuleNotFoundError`
**解决**:
```bash
cd backend
pip install -r requirements.txt
```

### 2. 前端启动失败

**问题**: `Cannot find module`
**解决**:
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### 3. 数据库连接失败

**问题**: `could not connect to server`
**解决**:
```bash
# 检查PostgreSQL是否运行
docker ps | grep postgres

# 重启PostgreSQL
docker restart valurise-postgres
```

### 4. Celery任务不执行

**问题**: 分析一直处于pending状态
**解决**:
```bash
# 检查Redis
redis-cli ping

# 检查Celery Worker日志
tail -f backend/celery.log
```

---

## 📖 文档索引

### 项目文档
- `README.md` - 项目总览
- `INTEGRATION_TEST_GUIDE.md` - 联调测试指南
- `QUICK_REFERENCE.md` - 本文档

### Week完成报告
- `项目文档/WEEK1_COMPLETION.md` - Week 1完成报告
- `项目文档/WEEK2_COMPLETION_REPORT.md` - Week 2完成报告
- `项目文档/WEEK3_COMPLETION_REPORT.md` - Week 3完成报告

### 技术文档
- `backend/README.md` - 后端开发文档
- `frontend/README.md` - 前端开发文档
- `backend/API_DEVELOPMENT_SUMMARY.md` - API开发总结

---

## 🔧 开发工具

### 推荐IDE
- **VSCode** + Python + TypeScript插件
- **PyCharm** (后端)
- **WebStorm** (前端)

### 推荐扩展
- Python
- Pylance
- ESLint
- Prettier
- Tailwind CSS IntelliSense

### 调试工具
- **后端**: FastAPI自带的/docs页面
- **前端**: React DevTools + Redux DevTools
- **数据库**: pgAdmin / DBeaver
- **API测试**: Postman / Insomnia

---

## 📞 获取帮助

### 查看日志

```bash
# FastAPI日志
tail -f logs/fastapi.log

# Celery日志
tail -f logs/celery.log

# Vite日志
tail -f logs/vite.log
```

### 检查服务状态

```bash
# 检查端口占用
netstat -an | grep -E "5173|8000|5432|6379"

# 检查Docker容器
docker ps

# 检查进程
ps aux | grep -E "uvicorn|celery|vite"
```

---

## 🎯 下一步

1. **完成联调测试**: 参考 `INTEGRATION_TEST_GUIDE.md`
2. **修复Bug**: 记录并修复测试中发现的问题
3. **准备部署**: 配置生产环境
4. **用户测试**: 招募测试用户

---

**祝开发顺利！** 🚀
