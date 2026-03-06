#!/bin/bash

# Celery Worker 启动脚本

echo "🔧 启动 Celery Worker..."

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "❌ 虚拟环境不存在"
    exit 1
fi

# 激活虚拟环境
source venv/bin/activate

# 检查Redis
echo "📡 检查Redis连接..."
redis-cli ping > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "⚠️  Redis未运行，请先启动Redis"
    echo "   提示: redis-server"
    echo "   或使用Docker: docker run -d -p 6379:6379 redis:7"
fi

# 启动Celery worker
echo "✅ 启动Celery worker..."
celery -A app.core.celery_app worker --loglevel=info --concurrency=2
