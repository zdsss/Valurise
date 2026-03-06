#!/bin/bash

# Valurise 停止所有服务脚本

set -e

echo "🛑 停止所有Valurise服务..."
echo "================================"
echo ""

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

# 停止前端
if [ -f .vite.pid ]; then
    VITE_PID=$(cat .vite.pid)
    echo "停止Vite (PID: $VITE_PID)..."
    kill $VITE_PID 2>/dev/null || echo "Vite已停止"
    rm .vite.pid
fi

# 停止后端
if [ -f .fastapi.pid ]; then
    FASTAPI_PID=$(cat .fastapi.pid)
    echo "停止FastAPI (PID: $FASTAPI_PID)..."
    kill $FASTAPI_PID 2>/dev/null || echo "FastAPI已停止"
    rm .fastapi.pid
fi

if [ -f .celery.pid ]; then
    CELERY_PID=$(cat .celery.pid)
    echo "停止Celery (PID: $CELERY_PID)..."
    kill $CELERY_PID 2>/dev/null || echo "Celery已停止"
    rm .celery.pid
fi

# 停止Docker容器
echo "停止Docker容器..."
docker stop valurise-postgres valurise-redis 2>/dev/null || echo "Docker容器已停止"

echo ""
echo -e "${GREEN}✅ 所有服务已停止${NC}"
echo ""
echo "💡 提示:"
echo "  - 如需删除Docker容器: docker rm valurise-postgres valurise-redis"
echo "  - 如需删除数据: docker volume prune"
