# 【桥见千年】一键部署脚本 (Windows PowerShell)
# 适用于 Windows 10/11

Write-Host "🌉 桥见千年 - Docker 部署脚本" -ForegroundColor Cyan
Write-Host "================================"

# 检查 Docker 是否安装
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Docker 未安装，请先安装 Docker Desktop" -ForegroundColor Red
    exit 1
}

# 检查 Docker 是否运行
$dockerStatus = docker info 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Docker 未运行，请先启动 Docker Desktop" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Docker 环境检查通过" -ForegroundColor Green

# 创建环境变量文件
if (-not (Test-Path .env)) {
    Write-Host "📝 创建 .env 文件..." -ForegroundColor Yellow
    Copy-Item .env.example .env
    Write-Host "⚠️  请编辑 .env 文件，填入 GLM_API_KEY" -ForegroundColor Yellow
}

# 构建镜像
Write-Host "🔨 构建 Docker 镜像..." -ForegroundColor Yellow
docker-compose build

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ 构建失败" -ForegroundColor Red
    exit 1
}

# 启动服务
Write-Host "🚀 启动服务..." -ForegroundColor Yellow
docker-compose up -d

# 等待服务启动
Write-Host "⏳ 等待服务启动..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# 检查服务状态
Write-Host "📊 服务状态:" -ForegroundColor Cyan
docker-compose ps

Write-Host ""
Write-Host "✅ 部署完成！" -ForegroundColor Green
Write-Host "🌐 访问地址: http://localhost" -ForegroundColor White
Write-Host "📚 后端API: http://localhost:5000" -ForegroundColor White
Write-Host ""
Write-Host "🛑 停止服务: docker-compose down" -ForegroundColor Gray
Write-Host "📋 查看日志: docker-compose logs -f" -ForegroundColor Gray
