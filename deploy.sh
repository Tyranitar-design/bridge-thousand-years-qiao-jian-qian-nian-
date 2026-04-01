#!/bin/bash

# 【桥见千年】一键部署脚本
# 适用于 Linux / macOS

echo "🌉 桥见千年 - Docker 部署脚本"
echo "================================"

# 检查 Docker 是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker 未安装，请先安装 Docker"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose 未安装，请先安装"
    exit 1
fi

echo "✅ Docker 环境检查通过"

# 创建环境变量文件（如果不存在）
if [ ! -f .env ]; then
    echo "📝 创建 .env 文件..."
    cp .env.example .env
    echo "⚠️  请编辑 .env 文件，填入 GLM_API_KEY"
fi

# 构建镜像
echo "🔨 构建 Docker 镜像..."
docker-compose build

# 启动服务
echo "🚀 启动服务..."
docker-compose up -d

# 等待服务启动
echo "⏳ 等待服务启动..."
sleep 5

# 检查服务状态
echo "📊 服务状态:"
docker-compose ps

echo ""
echo "✅ 部署完成！"
echo "🌐 访问地址: http://localhost"
echo "📚 后端API: http://localhost:5000"
echo ""
echo "🛑 停止服务: docker-compose down"
echo "📋 查看日志: docker-compose logs -f"
