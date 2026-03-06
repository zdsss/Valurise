#!/bin/bash

# Valurise 快速启动脚本
# 用于启动所有必要的服务进行联调测试

set -e

echo "🚀 Valurise 联调测试 - 快速启动"
echo "================================"
echo ""

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 检查Docker是否安装
check_docker() {
    if ! command -v docker &> /dev/null; then
        echo -e "${RED}❌ Docker未安装${NC}"
        echo "请先安装Docker: https://docs.docker.com/get-docker/"
        exit 1
    fi
    echo -e "${GREEN}✅ Docker已安装${NC}"
}

# 启动PostgreSQL
start_postgres() {
    echo ""
    echo "📦 启动PostgreSQL..."

    if docker ps -a | grep -q valurise-postgres; then
        echo "容器已存在，正在启动..."
        docker start valurise-postgres
    else
        echo "创建新容器..."
        docker run -d --name valurise-postgres \
            -e POSTGRES_DB=valurise \
            -e POSTGRES_USER=valurise \
            -e POSTGRES_PASSWORD=password \
            -p 5432:5432 \
            postgres:15
    fi

    echo -e "${GREEN}✅ PostgreSQL已启动${NC}"
    echo "   连接信息: postgresql://valurise:password@localhost:5432/valurise"
}

# 启动Redis
start_redis() {
    echo ""
    echo "📦 启动Redis..."

    if docker ps -a | grep -q valurise-redis; then
        echo "容器已存在，正在启动..."
        docker start valurise-redis
    else
        echo "创建新容器..."
        docker run -d --name valurise-redis \
            -p 6379:6379 \
            redis:7
    fi

    echo -e "${GREEN}✅ Redis已启动${NC}"
    echo "   连接信息: redis://localhost:6379/0"
}

# 等待服务就绪
wait_for_services() {
    echo ""
    echo "⏳ 等待服务就绪..."
    sleep 3
    echo -e "${GREEN}✅ 服务已就绪${NC}"
}

# 启动后端
start_backend() {
    echo ""
    echo "🔧 启动后端服务..."

    cd backend

    # 检查环境变量
    if [ ! -f .env ]; then
        echo -e "${YELLOW}⚠️  .env文件不存在，从.env.example复制${NC}"
        cp .env.example .env
    fi

    # 启动FastAPI（后台运行）
    echo "启动FastAPI..."
    chmod +x start.sh
    ./start.sh > ../logs/fastapi.log 2>&1 &
    FASTAPI_PID=$!
    echo "FastAPI PID: $FASTAPI_PID"

    # 等待FastAPI启动
    sleep 5

    # 启动Celery Worker（后台运行）
    echo "启动Celery Worker..."
    chmod +x start_worker.sh
    ./start_worker.sh > ../logs/celery.log 2>&1 &
    CELERY_PID=$!
    echo "Celery PID: $CELERY_PID"

    cd ..

    echo -e "${GREEN}✅ 后端服务已启动${NC}"
    echo "   FastAPI: http://localhost:8000"
    echo "   API文档: http://localhost:8000/docs"
    echo "   FastAPI PID: $FASTAPI_PID"
    echo "   Celery PID: $CELERY_PID"

    # 保存PID
    echo $FASTAPI_PID > .fastapi.pid
    echo $CELERY_PID > .celery.pid
}

# 启动前端
start_frontend() {
    echo ""
    echo "🎨 启动前端服务..."

    cd frontend

    # 检查环境变量
    if [ ! -f .env ]; then
        echo -e "${YELLOW}⚠️  .env文件不存在，创建默认配置${NC}"
        echo "VITE_API_URL=http://localhost:8000/api/v1" > .env
    fi

    # 检查依赖
    if [ ! -d node_modules ]; then
        echo "安装依赖..."
        npm install
    fi

    # 启动Vite（后台运行）
    echo "启动Vite开发服务器..."
    npm run dev > ../logs/vite.log 2>&1 &
    VITE_PID=$!
    echo "Vite PID: $VITE_PID"

    cd ..

    echo -e "${GREEN}✅ 前端服务已启动${NC}"
    echo "   前端: http://localhost:5173"
    echo "   Vite PID: $VITE_PID"

    # 保存PID
    echo $VITE_PID > .vite.pid
}

# 显示状态
show_status() {
    echo ""
    echo "================================"
    echo "🎉 所有服务已启动！"
    echo "================================"
    echo ""
    echo "📊 服务状态:"
    echo "  - PostgreSQL: http://localhost:5432"
    echo "  - Redis: http://localhost:6379"
    echo "  - FastAPI: http://localhost:8000"
    echo "  - API文档: http://localhost:8000/docs"
    echo "  - 前端: http://localhost:5173"
    echo ""
    echo "📝 日志文件:"
    echo "  - FastAPI: logs/fastapi.log"
    echo "  - Celery: logs/celery.log"
    echo "  - Vite: logs/vite.log"
    echo ""
    echo "🛑 停止所有服务:"
    echo "  ./stop_all.sh"
    echo ""
    echo "📖 测试指南:"
    echo "  查看 INTEGRATION_TEST_GUIDE.md"
    echo ""
}

# 创建日志目录
mkdir -p logs

# 主流程
main() {
    check_docker
    start_postgres
    start_redis
    wait_for_services
    start_backend
    start_frontend
    show_status
}

# 错误处理
trap 'echo -e "${RED}❌ 启动失败${NC}"; exit 1' ERR

# 执行主流程
main
