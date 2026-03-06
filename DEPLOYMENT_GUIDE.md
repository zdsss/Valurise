# Valurise 部署指南

**版本**: 1.0
**日期**: 2026年3月6日
**状态**: 生产就绪

---

## 📋 部署前检查

### 前端 ✅
- ✅ 生产构建成功
- ✅ 包大小: 151KB (gzip)
- ✅ Meta标签完整
- ✅ 错误处理完善
- ✅ 所有测试通过

### 后端 ✅
- ✅ 代码完成
- ✅ API端点完整
- ✅ Agent系统就绪
- ⏳ 环境配置待完成

---

## 🚀 部署方案

### 推荐方案: Vercel + Railway

**优点**:
- 🚀 部署简单快速
- 💰 免费额度充足
- 🔄 自动CI/CD
- 📊 内置监控
- 🌍 全球CDN

**成本**:
- Vercel: 免费（Hobby计划）
- Railway: $5/月起

---

## 📦 方案1: Vercel (前端) + Railway (后端)

### 1.1 前端部署到Vercel

#### 步骤1: 准备代码
```bash
cd frontend

# 确保.env.example存在
cat > .env.example << EOF
VITE_API_URL=https://your-api-domain.railway.app/api/v1
EOF

# 提交到Git
git add .
git commit -m "Prepare for deployment"
git push
```

#### 步骤2: 部署到Vercel
```bash
# 安装Vercel CLI
npm i -g vercel

# 登录
vercel login

# 部署
vercel --prod
```

**或使用Vercel Dashboard**:
1. 访问 https://vercel.com
2. 导入GitHub仓库
3. 选择 `frontend` 目录
4. 配置环境变量:
   - `VITE_API_URL`: 后端API地址
5. 点击Deploy

#### 步骤3: 配置自定义域名（可选）
1. 在Vercel Dashboard添加域名
2. 配置DNS记录
3. 等待SSL证书生成

### 1.2 后端部署到Railway

#### 步骤1: 准备Railway
1. 访问 https://railway.app
2. 使用GitHub登录
3. 创建新项目

#### 步骤2: 添加数据库服务
```bash
# 在Railway Dashboard:
1. 点击 "New" → "Database" → "PostgreSQL"
2. 点击 "New" → "Database" → "Redis"
3. 等待服务启动
```

#### 步骤3: 部署后端
```bash
# 在Railway Dashboard:
1. 点击 "New" → "GitHub Repo"
2. 选择Valurise仓库
3. 选择 backend 目录
4. Railway自动检测Python项目
```

#### 步骤4: 配置环境变量
在Railway Dashboard配置:
```bash
# 数据库（自动生成）
DATABASE_URL=${{Postgres.DATABASE_URL}}
REDIS_URL=${{Redis.REDIS_URL}}

# Anthropic API
ANTHROPIC_API_KEY=sk-ant-your-key-here
MODEL_MAIN=claude-sonnet-4-6
MODEL_FAST=claude-haiku-4-6

# JWT
JWT_SECRET=your-random-secret-key-here
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
REFRESH_TOKEN_EXPIRE_DAYS=30

# Stripe
STRIPE_SECRET_KEY=sk_live_your-stripe-key
STRIPE_WEBHOOK_SECRET=whsec_your-webhook-secret
STRIPE_PRICE_BASIC=price_basic_id
STRIPE_PRICE_PRO=price_pro_id
STRIPE_PRICE_PREMIUM=price_premium_id

# CORS
CORS_ORIGINS=["https://your-frontend-domain.vercel.app"]

# App
DEBUG=False
```

#### 步骤5: 启动服务
Railway会自动:
1. 安装依赖 (`pip install -r requirements.txt`)
2. 运行数据库迁移
3. 启动服务

#### 步骤6: 配置Celery Worker
```bash
# 在Railway Dashboard:
1. 复制后端服务
2. 修改启动命令为:
   celery -A app.core.celery_app worker --loglevel=info
3. 使用相同的环境变量
```

---

## 🐳 方案2: Docker部署

### 2.1 创建Docker配置

#### 前端Dockerfile
```dockerfile
# frontend/Dockerfile
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

#### 前端Nginx配置
```nginx
# frontend/nginx.conf
server {
    listen 80;
    server_name _;
    root /usr/share/nginx/html;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /assets {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

#### 后端Dockerfile
```dockerfile
# backend/Dockerfile
FROM python:3.11-slim
WORKDIR /app

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制代码
COPY . .

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### Docker Compose
```yaml
# docker-compose.yml
version: '3.8'

services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: valurise
      POSTGRES_USER: valurise
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  backend:
    build: ./backend
    environment:
      DATABASE_URL: postgresql://valurise:${DB_PASSWORD}@postgres:5432/valurise
      REDIS_URL: redis://redis:6379/0
      ANTHROPIC_API_KEY: ${ANTHROPIC_API_KEY}
      JWT_SECRET: ${JWT_SECRET}
      STRIPE_SECRET_KEY: ${STRIPE_SECRET_KEY}
    depends_on:
      - postgres
      - redis
    ports:
      - "8000:8000"

  celery:
    build: ./backend
    command: celery -A app.core.celery_app worker --loglevel=info
    environment:
      DATABASE_URL: postgresql://valurise:${DB_PASSWORD}@postgres:5432/valurise
      REDIS_URL: redis://redis:6379/0
      ANTHROPIC_API_KEY: ${ANTHROPIC_API_KEY}
    depends_on:
      - postgres
      - redis

  frontend:
    build: ./frontend
    ports:
      - "80:80"
    depends_on:
      - backend

volumes:
  postgres_data:
```

### 2.2 部署步骤
```bash
# 1. 创建.env文件
cat > .env << EOF
DB_PASSWORD=your-secure-password
ANTHROPIC_API_KEY=your-api-key
JWT_SECRET=your-jwt-secret
STRIPE_SECRET_KEY=your-stripe-key
EOF

# 2. 构建和启动
docker-compose up -d

# 3. 查看日志
docker-compose logs -f

# 4. 停止服务
docker-compose down
```

---

## 🖥️ 方案3: VPS部署

### 3.1 服务器要求
- OS: Ubuntu 22.04 LTS
- RAM: 2GB+
- CPU: 2核+
- 存储: 20GB+

### 3.2 安装依赖
```bash
# 更新系统
sudo apt update && sudo apt upgrade -y

# 安装Node.js 20
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs

# 安装Python 3.11
sudo apt install -y python3.11 python3.11-venv python3-pip

# 安装PostgreSQL
sudo apt install -y postgresql postgresql-contrib

# 安装Redis
sudo apt install -y redis-server

# 安装Nginx
sudo apt install -y nginx
```

### 3.3 配置数据库
```bash
# 创建数据库
sudo -u postgres psql
CREATE DATABASE valurise;
CREATE USER valurise WITH PASSWORD 'your-password';
GRANT ALL PRIVILEGES ON DATABASE valurise TO valurise;
\q
```

### 3.4 部署后端
```bash
# 克隆代码
cd /opt
sudo git clone https://github.com/your-repo/valurise.git
cd valurise/backend

# 创建虚拟环境
python3.11 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
sudo nano .env

# 创建systemd服务
sudo nano /etc/systemd/system/valurise-api.service
```

**valurise-api.service**:
```ini
[Unit]
Description=Valurise API
After=network.target postgresql.service redis.service

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/valurise/backend
Environment="PATH=/opt/valurise/backend/venv/bin"
ExecStart=/opt/valurise/backend/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

**valurise-celery.service**:
```ini
[Unit]
Description=Valurise Celery Worker
After=network.target redis.service

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/valurise/backend
Environment="PATH=/opt/valurise/backend/venv/bin"
ExecStart=/opt/valurise/backend/venv/bin/celery -A app.core.celery_app worker --loglevel=info
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# 启动服务
sudo systemctl daemon-reload
sudo systemctl enable valurise-api valurise-celery
sudo systemctl start valurise-api valurise-celery
```

### 3.5 部署前端
```bash
# 构建前端
cd /opt/valurise/frontend
npm ci
npm run build

# 复制到Nginx目录
sudo cp -r dist/* /var/www/valurise/
```

### 3.6 配置Nginx
```nginx
# /etc/nginx/sites-available/valurise
server {
    listen 80;
    server_name your-domain.com;

    # 前端
    location / {
        root /var/www/valurise;
        try_files $uri $uri/ /index.html;
    }

    # 后端API
    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
# 启用站点
sudo ln -s /etc/nginx/sites-available/valurise /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 3.7 配置HTTPS
```bash
# 安装Certbot
sudo apt install -y certbot python3-certbot-nginx

# 获取SSL证书
sudo certbot --nginx -d your-domain.com

# 自动续期
sudo systemctl enable certbot.timer
```

---

## 🔒 安全配置

### 环境变量安全
- ✅ 使用强随机密钥
- ✅ 不要提交.env到Git
- ✅ 使用密钥管理服务（可选）

### 数据库安全
- ✅ 使用强密码
- ✅ 限制网络访问
- ✅ 定期备份

### API安全
- ✅ 启用HTTPS
- ✅ 配置CORS
- ✅ 限流保护
- ✅ 输入验证

---

## 📊 监控和日志

### 应用监控
- Vercel Analytics（前端）
- Railway Metrics（后端）
- Sentry（错误追踪）

### 日志管理
```bash
# 查看后端日志
sudo journalctl -u valurise-api -f

# 查看Celery日志
sudo journalctl -u valurise-celery -f

# 查看Nginx日志
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

---

## 🔄 更新部署

### Vercel更新
```bash
# 推送到GitHub，自动部署
git push origin main
```

### Railway更新
```bash
# 推送到GitHub，自动部署
git push origin main
```

### VPS更新
```bash
# 拉取最新代码
cd /opt/valurise
sudo git pull

# 更新后端
cd backend
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart valurise-api valurise-celery

# 更新前端
cd ../frontend
npm ci
npm run build
sudo cp -r dist/* /var/www/valurise/
```

---

## 📝 部署检查清单

### 部署前 ✅
- [ ] 代码测试通过
- [ ] 环境变量配置
- [ ] 数据库准备
- [ ] API密钥获取
- [ ] 域名准备

### 部署中 ⏳
- [ ] 前端部署
- [ ] 后端部署
- [ ] 数据库迁移
- [ ] Celery启动
- [ ] DNS配置

### 部署后 ⏳
- [ ] 功能测试
- [ ] 性能测试
- [ ] 安全检查
- [ ] 监控配置
- [ ] 备份配置

---

**文档版本**: 1.0
**最后更新**: 2026年3月6日
**维护者**: Kiro AI Assistant
