#!/bin/bash

# Valurise Backend 启动脚本

echo "🚀 启动 Valurise Backend..."

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "❌ 虚拟环境不存在，请先运行: python -m venv venv"
    exit 1
fi

# 激活虚拟环境
source venv/bin/activate

# 检查依赖
echo "📦 检查依赖..."
pip list | grep fastapi > /dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  依赖未安装，正在安装..."
    pip install -r requirements.txt
fi

# 检查环境变量
if [ ! -f ".env" ]; then
    echo "❌ .env文件不存在，请先配置环境变量"
    echo "   提示: cp .env.example .env"
    exit 1
fi

# 启动应用
echo "✅ 启动FastAPI应用..."
echo "📝 API文档: http://localhost:8000/docs"
echo ""

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
