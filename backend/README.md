# Valurise Backend

AI驱动的职业价值发现平台 - 后端API服务

## 📋 项目概述

基于FastAPI构建的RESTful API服务，提供用户认证、职业分析、支付处理等核心功能。

## 🏗️ 技术栈

- **框架**: FastAPI 0.115.0
- **数据库**: PostgreSQL + SQLAlchemy
- **认证**: JWT + bcrypt
- **支付**: Stripe
- **任务队列**: Celery + Redis
- **AI服务**: Anthropic Claude API

## 📁 项目结构

```
backend/
├── app/
│   ├── main.py                 # FastAPI应用入口
│   ├── config.py               # 配置管理
│   ├── database.py             # 数据库连接
│   ├── models/                 # SQLAlchemy模型
│   │   ├── user.py
│   │   ├── analysis.py
│   │   └── order.py
│   ├── schemas/                # Pydantic schemas
│   │   ├── user.py
│   │   ├── analysis.py
│   │   └── order.py
│   ├── api/                    # API路由
│   │   ├── auth.py
│   │   ├── analysis.py
│   │   ├── payment.py
│   │   └── users.py
│   ├── core/                   # 核心功能
│   │   ├── security.py
│   │   └── celery_app.py
│   └── services/               # 业务逻辑
│       ├── agent_service.py
│       └── payment_service.py
├── agents_optimized.py         # 优化后的Agent
├── requirements.txt            # Python依赖
├── .env                        # 环境变量
└── README.md                   # 本文档
```

## 🚀 快速开始

### 1. 安装依赖

```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt
```

### 2. 配置环境变量

复制 `.env.example` 到 `.env` 并填写配置：

```bash
cp .env.example .env
```

必需配置：
- `ANTHROPIC_API_KEY`: Anthropic API密钥
- `DATABASE_URL`: PostgreSQL连接字符串
- `JWT_SECRET`: JWT密钥
- `STRIPE_SECRET_KEY`: Stripe密钥

### 3. 初始化数据库

```bash
# 确保PostgreSQL正在运行
# 创建数据库
createdb valurise

# 运行应用（自动创建表）
python -m app.main
```

### 4. 启动服务

```bash
# 开发模式（自动重载）
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 生产模式
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### 5. 访问API文档

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- OpenAPI JSON: http://localhost:8000/openapi.json

## 📡 API端点

### 认证相关

- `POST /api/v1/auth/register` - 用户注册
- `POST /api/v1/auth/login` - 用户登录
- `POST /api/v1/auth/refresh` - 刷新token

### 分析相关

- `POST /api/v1/analyses` - 创建分析任务
- `GET /api/v1/analyses/{id}` - 获取分析状态
- `GET /api/v1/analyses/{id}/result` - 获取分析结果
- `GET /api/v1/analyses` - 获取历史记录

### 支付相关

- `POST /api/v1/payment/create-checkout` - 创建支付会话
- `POST /api/v1/payment/webhook` - Stripe webhook
- `GET /api/v1/payment/verify/{session_id}` - 验证支付

### 用户相关

- `GET /api/v1/users/me` - 获取当前用户信息
- `PATCH /api/v1/users/me` - 更新用户信息

## 🗄️ 数据库模型

### User (用户)
- id, email, hashed_password
- subscription_tier, credits_remaining
- created_at, updated_at

### Analysis (分析任务)
- id, user_id, status
- input_data, target_role
- extracted_info, value_analysis, narrative_strategy, resume_versions
- cost, processing_time_seconds
- created_at, started_at, completed_at

### Order (订单)
- id, user_id, analysis_id
- stripe_checkout_session_id, stripe_payment_intent_id
- product_tier, amount_cents, status
- created_at, paid_at

## 🔐 认证方案

使用JWT Bearer Token认证：

```bash
# 登录获取token
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"password"}'

# 使用token访问受保护端点
curl -X GET http://localhost:8000/api/v1/users/me \
  -H "Authorization: Bearer <access_token>"
```

## 🧪 测试

```bash
# 运行所有测试
pytest

# 运行特定测试
pytest tests/test_auth.py

# 生成覆盖率报告
pytest --cov=app tests/
```

## 📊 监控

### 健康检查

```bash
curl http://localhost:8000/health
```

### 日志

日志输出到标准输出，可以使用日志聚合工具收集。

## 🚀 部署

### Railway部署

1. 连接GitHub仓库
2. 添加PostgreSQL服务
3. 添加Redis服务
4. 配置环境变量
5. 自动部署

### Docker部署

```bash
# 构建镜像
docker build -t valurise-backend .

# 运行容器
docker run -p 8000:8000 --env-file .env valurise-backend
```

## 🔧 开发指南

### 添加新的API端点

1. 在 `app/api/` 创建路由文件
2. 在 `app/schemas/` 定义请求/响应模型
3. 在 `app/main.py` 注册路由

### 添加新的数据库模型

1. 在 `app/models/` 创建模型文件
2. 在 `app/models/__init__.py` 导出模型
3. 运行数据库迁移

### 代码风格

- 使用 `black` 格式化代码
- 使用 `flake8` 检查代码质量
- 使用 `mypy` 进行类型检查

## 📝 环境变量说明

| 变量名 | 说明 | 必需 | 默认值 |
|--------|------|------|--------|
| ANTHROPIC_API_KEY | Anthropic API密钥 | ✅ | - |
| DATABASE_URL | PostgreSQL连接字符串 | ✅ | - |
| REDIS_URL | Redis连接字符串 | ✅ | redis://localhost:6379/0 |
| JWT_SECRET | JWT密钥 | ✅ | - |
| STRIPE_SECRET_KEY | Stripe密钥 | ✅ | - |
| DEBUG | 调试模式 | ❌ | True |
| CORS_ORIGINS | CORS允许的源 | ❌ | ["http://localhost:3000"] |

## 🐛 故障排除

### 数据库连接失败

检查PostgreSQL是否运行：
```bash
pg_isready
```

检查连接字符串格式：
```
postgresql://user:password@host:port/database
```

### API调用失败

检查Anthropic API密钥是否正确：
```bash
echo $ANTHROPIC_API_KEY
```

检查网络连接和代理设置。

## 📚 相关文档

- [FastAPI文档](https://fastapi.tiangolo.com/)
- [SQLAlchemy文档](https://docs.sqlalchemy.org/)
- [Stripe文档](https://stripe.com/docs/api)
- [Anthropic文档](https://docs.anthropic.com/)

## 📞 支持

- 技术问题: dev@valurise.com
- 文档: https://docs.valurise.com
- GitHub: https://github.com/valurise/backend

---

**版本**: 1.0.0
**最后更新**: 2026年3月5日
