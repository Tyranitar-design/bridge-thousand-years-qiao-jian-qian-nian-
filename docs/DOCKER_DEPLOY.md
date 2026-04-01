# Docker 部署指南

本文档介绍如何使用 Docker 部署【桥见千年】项目。

## 📋 前置要求

- Docker Engine 20.10+
- Docker Compose 2.0+
- 至少 2GB 可用内存

### 安装 Docker

**Windows / macOS**:
- 下载并安装 [Docker Desktop](https://www.docker.com/products/docker-desktop)

**Linux (Ubuntu)**:
```bash
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER
```

## 🚀 快速部署

### 1. 克隆项目

```bash
git clone https://github.com/your-username/bridge-thousand-years.git
cd bridge-thousand-years
```

### 2. 配置环境变量

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env 文件
nano .env
```

在 `.env` 文件中填入 GLM API Key：
```
GLM_API_KEY=your_actual_api_key_here
```

### 3. 一键部署

**Linux / macOS**:
```bash
chmod +x deploy.sh
./deploy.sh
```

**Windows PowerShell**:
```powershell
.\deploy.ps1
```

### 4. 访问应用

- 前端：http://localhost
- 后端API：http://localhost:5000

## 🔧 手动部署

如果一键脚本无法运行，可手动执行：

```bash
# 构建镜像
docker-compose build

# 启动服务
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

## 📦 镜像说明

### 前端镜像

- 基础镜像：`nginx:alpine`
- 构建阶段：`node:18-alpine`
- 暴露端口：80
- 静态文件目录：`/usr/share/nginx/html`

### 后端镜像

- 基础镜像：`python:3.9-slim`
- 暴露端口：5000
- 工作目录：`/app`

## 🔍 故障排查

### 端口被占用

```bash
# 查看端口占用
lsof -i :80      # Linux/macOS
netstat -ano | findstr :80  # Windows

# 修改 docker-compose.yml 中的端口映射
ports:
  - "8080:80"    # 改为其他端口
```

### 镜像构建失败

```bash
# 清理 Docker 缓存
docker system prune -a

# 重新构建
docker-compose build --no-cache
```

### 服务无法访问

```bash
# 检查容器状态
docker-compose ps

# 查看容器日志
docker-compose logs frontend
docker-compose logs backend

# 进入容器调试
docker exec -it bridge-frontend sh
docker exec -it bridge-backend bash
```

## 🌐 生产环境配置

### 使用 HTTPS

1. 准备 SSL 证书
2. 修改 `frontend/nginx.conf`：

```nginx
server {
    listen 443 ssl;
    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;
    # ...
}
```

3. 更新 `docker-compose.yml` 挂载证书

### 环境变量

```yaml
environment:
  - FLASK_ENV=production
  - GLM_API_KEY=${GLM_API_KEY}
```

## 📊 性能优化

### 前端优化

- Gzip 压缩已在 nginx 中配置
- 静态资源缓存 1 年
- 使用 alpine 基础镜像减小体积

### 后端优化

- 使用 gunicorn（生产环境）：

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

## 🔄 更新部署

```bash
# 拉取最新代码
git pull

# 重新构建并启动
docker-compose up -d --build
```

## 🗑️ 清理资源

```bash
# 停止并删除容器
docker-compose down

# 删除镜像
docker rmi bridge-thousand-years_frontend
docker rmi bridge-thousand-years_backend

# 清理所有未使用资源
docker system prune -a
```

---

如有问题，请提交 Issue 或联系团队。
