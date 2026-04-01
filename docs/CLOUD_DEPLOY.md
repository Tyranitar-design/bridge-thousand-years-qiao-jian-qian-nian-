# 云服务部署指南

本指南帮助你在云端部署【桥见千年】项目，获得在线演示地址。

---

## 🎯 部署方案

| 服务 | 用途 | 费用 | 地址 |
|------|------|------|------|
| **Vercel** | 前端部署 | 免费 | vercel.com |
| **Render** | 后端部署 | 免费 | render.com |

---

## 第一部分：后端部署（Render）

### 步骤1：注册Render账号

1. 访问 https://dashboard.render.com/
2. 点击 **Get Started**
3. 使用GitHub账号登录（推荐）

### 步骤2：创建Web Service

1. 点击 **New** → **Web Service**
2. 连接你的GitHub仓库：`bridge-thousand-years-qiao-jian-qian-nian-`
3. 配置服务：

| 配置项 | 值 |
|--------|------|
| Name | `bridge-backend` |
| Region | `Singapore` (离中国最近) |
| Branch | `main` |
| Root Directory | `backend` |
| Runtime | `Python 3` |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `python run.py` |

### 步骤3：配置环境变量

在 **Environment Variables** 中添加：

```
GLM_API_KEY=你的GLM_API_KEY
FLASK_ENV=production
```

### 步骤4：部署

1. 点击 **Create Web Service**
2. 等待构建完成（约3-5分钟）
3. 获得后端地址：`https://bridge-backend.onrender.com`

---

## 第二部分：前端部署（Vercel）

### 步骤1：注册Vercel账号

1. 访问 https://vercel.com/
2. 点击 **Sign Up**
3. 使用GitHub账号登录

### 步骤2：导入项目

1. 点击 **Add New** → **Project**
2. 选择 `bridge-thousand-years-qiao-jian-qian-nian-` 仓库
3. 配置项目：

| 配置项 | 值 |
|--------|------|
| Framework Preset | `Vite` |
| Root Directory | `frontend` |
| Build Command | `npm run build` |
| Output Directory | `dist` |

### 步骤3：配置环境变量

在 **Environment Variables** 中添加：

```
VITE_API_URL=https://bridge-backend.onrender.com
```

### 步骤4：部署

1. 点击 **Deploy**
2. 等待构建完成（约1-2分钟）
3. 获得前端地址：`https://bridge-thousand-years.vercel.app`

---

## 第三部分：更新API配置

### 修改前端API地址

在你的本地项目中，修改 `frontend/src/api/index.js`：

```javascript
// API 基础地址
const baseURL = import.meta.env.VITE_API_URL || 'http://localhost:5000'
```

然后提交更新：

```powershell
cd "D:\AI创意大赛\【桥见千年】中国古代桥梁智慧可视化平台"
git add .
git commit -m "feat: 配置云服务API地址"
git push
```

Vercel会自动重新部署。

---

## 📊 部署完成后

### 访问地址

- 前端：`https://bridge-thousand-years.vercel.app`
- 后端：`https://bridge-backend.onrender.com`

### 比赛提交

| 提交项 | 内容 |
|--------|------|
| 可运行文件 | GitHub仓库地址 |
| 可访问地址 | Vercel前端地址 |

---

## ⚠️ 注意事项

### Render 冷启动

Render免费版会有冷启动问题：
- 超过15分钟无请求会休眠
- 首次访问需要等待30秒左右唤醒

### 解决方案

1. 使用定时服务每10分钟ping一次后端
2. 或在Vercel前端添加加载提示

---

## 🔗 快速链接

- Vercel Dashboard: https://vercel.com/dashboard
- Render Dashboard: https://dashboard.render.com/
- 项目GitHub: https://github.com/Tyranitar-design/bridge-thousand-years-qiao-jian-qian-nian-

---

**部署预计耗时**：15-20分钟

祝部署顺利！🚀
