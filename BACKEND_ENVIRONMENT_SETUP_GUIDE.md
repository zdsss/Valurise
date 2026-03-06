# 后端环境配置实施指南

**日期**: 2026年3月6日
**状态**: 环境缺失，需要配置

---

## 🔍 当前环境检查结果

### 已安装
- ✅ Python 3.13.11
- ✅ Node.js 18.20.4
- ✅ MySQL Server 8.0（在PATH中）

### 未安装
- ❌ Docker
- ❌ PostgreSQL
- ❌ Redis

---

## 🎯 推荐方案：使用Railway（在线部署）

### 为什么选择Railway？
1. **无需本地安装**：不需要安装PostgreSQL和Redis
2. **快速配置**：5-10分钟完成
3. **免费额度**：$5免费额度
4. **自动管理**：数据库自动备份和维护
5. **生产就绪**：直接可用于生产环境

### Railway配置步骤

#### 步骤1：注册Railway账号
1. 访问 https://railway.app
2. 使用GitHub账号登录
3. 验证邮箱

#### 步骤2：创建项目
1. 点击 "New Project"
2. 选择 "Empty Project"
3. 命名为 "valurise"

#### 步骤3：添加PostgreSQL
1. 点击 "+ New"
2. 选择 "Database"
3. 选择 "PostgreSQL"
4. 等待部署完成（1-2分钟）
5. 点击PostgreSQL服务
6. 复制 "DATABASE_URL"

#### 步骤4：添加Redis
1. 点击 "+ New"
2. 选择 "Database"
3. 选择 "Redis"
4. 等待部署完成（1-2分钟）
5. 点击Redis服务
6. 复制 "REDIS_URL"

#### 步骤5：配置后端环境变量
创建/更新 `backend/.env` 文件：

```bash
# 从Railway复制的数据库URL
DATABASE_URL=postgresql://postgres:xxx@xxx.railway.app:5432/railway
REDIS_URL=redis://default:xxx@xxx.railway.app:6379

# Anthropic API（已有）
ANTHROPIC_API_KEY=sk-JBjltQd00P8AsV71Y8njeiw7iby5iaExG79Wfnkh2IM9X5ny
MODEL_MAIN=claude-sonnet-4-6
MODEL_FAST=claude-haiku-4-6

# JWT配置（生成随机密钥）
JWT_SECRET=your-random-secret-key-here-change-this
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
REFRESH_TOKEN_EXPIRE_DAYS=30

# Stripe配置（测试模式）
STRIPE_SECRET_KEY=sk_test_your_stripe_test_key
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret
STRIPE_PRICE_BASIC=price_basic_id
STRIPE_PRICE_PRO=price_pro_id
STRIPE_PRICE_PREMIUM=price_premium_id

# App配置
APP_NAME=Valurise
APP_VERSION=1.0.0
DEBUG=True
CORS_ORIGINS=["http://localhost:5173","http://localhost:4173"]
API_V1_PREFIX=/api/v1

# Cost Tracking
TARGET_COST_PER_RUN=2.00
```

#### 步骤6：启动后端服务
```bash
cd backend

# 安装依赖（如果还没安装）
pip install -r requirements.txt

# 启动FastAPI服务
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### 步骤7：启动Celery Worker（新终端）
```bash
cd backend

# 启动Worker
celery -A app.core.celery_app worker --loglevel=info
```

---

## 🔄 替代方案1：使用SQLite（快速测试）

如果只是想快速测试，可以临时使用SQLite：

### 修改配置
```python
# backend/app/config.py
# 临时使用SQLite
DATABASE_URL = "sqlite:///./valurise.db"
```

### 限制
- ❌ 不支持并发写入
- ❌ 不适合生产环境
- ❌ Celery仍需要Redis
- ✅ 可以快速测试API

---

## 🔄 替代方案2：安装本地环境

### Windows安装PostgreSQL
1. 下载：https://www.postgresql.org/download/windows/
2. 运行安装程序
3. 设置密码
4. 创建数据库：
```bash
# 使用pgAdmin或命令行
createdb valurise
```

### Windows安装Redis
1. 下载：https://github.com/microsoftarchive/redis/releases
2. 解压并运行 redis-server.exe
3. 或使用WSL2安装Redis

### 配置环境变量
```bash
DATABASE_URL=postgresql://postgres:password@localhost:5432/valurise
REDIS_URL=redis://localhost:6379/0
```

---

## 🔄 替代方案3：使用MySQL（已安装）

系统中已有MySQL，可以临时使用：

### 修改依赖
```bash
# backend/requirements.txt
# 替换 psycopg2-binary 为
pymysql==1.1.0
```

### 修改配置
```bash
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/valurise
```

### 创建数据库
```bash
mysql -u root -p
CREATE DATABASE valurise;
```

### 限制
- ⚠️ 需要修改部分代码（PostgreSQL特定功能）
- ⚠️ 仍需要Redis

---

## 📋 推荐执行顺序

### 最快方案（推荐）：Railway
**时间**：10-15分钟
**优点**：无需本地安装，生产就绪
**步骤**：
1. 注册Railway（2分钟）
2. 创建PostgreSQL和Redis（5分钟）
3. 配置.env文件（2分钟）
4. 启动后端服务（1分钟）
5. 测试API（5分钟）

### 快速测试方案：SQLite + 跳过Celery
**时间**：5分钟
**优点**：最快
**限制**：无法测试异步任务
**步骤**：
1. 修改配置使用SQLite
2. 启动FastAPI
3. 测试基础API

### 完整本地方案：安装PostgreSQL + Redis
**时间**：30-60分钟
**优点**：完全本地控制
**步骤**：
1. 安装PostgreSQL（15分钟）
2. 安装Redis（15分钟）
3. 配置环境（10分钟）
4. 启动服务（5分钟）

---

## 🎯 我的建议

**推荐使用Railway方案**，原因：
1. ✅ 最快（10-15分钟）
2. ✅ 无需本地安装
3. ✅ 生产就绪
4. ✅ 免费额度充足
5. ✅ 可以直接部署后端

**下一步**：
1. 你去Railway注册账号
2. 创建PostgreSQL和Redis
3. 把DATABASE_URL和REDIS_URL告诉我
4. 我配置.env并启动后端
5. 开始测试

---

## 📞 需要帮助？

如果你选择：
- **Railway方案**：我可以指导每一步
- **本地安装**：我可以提供详细命令
- **快速测试**：我可以修改代码使用SQLite

**你想使用哪个方案？**
