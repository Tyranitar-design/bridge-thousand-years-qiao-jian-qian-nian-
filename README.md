# 【桥见千年】中国古代桥梁智慧可视化平台

> 🌉 桥见千年，连接古今——用AI与可视化技术，让千年桥梁智慧焕发新生

[![Vue](https://img.shields.io/badge/Vue-3.5-brightgreen)](https://vuejs.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0-green)](https://flask.palletsprojects.com/)
[![Three.js](https://img.shields.io/badge/Three.js-0.183-orange)](https://threejs.org/)
[![License](https://img.shields.io/badge/License-MIT-blue)](LICENSE)

## 📖 项目简介

本项目是**信息管理学院"AI领航·创见无限"AI创意主题大赛**参赛作品，聚焦1911年前中国古代桥梁成就，运用AI技术与现代可视化手段，打造集知识传播、互动体验、智能问答于一体的数字化平台。

### 核心价值

- 🏛️ **建筑成就展示**：31座中国古代著名桥梁完整数据
- 👨‍🔧 **工匠精神传承**：桥梁建造者传记与精神解读
- 🤖 **AI智能问答**：GLM-4大模型驱动的知识对话
- 🎮 **沉浸式体验**：3D模型、建造模拟、知识挑战

## ✨ 功能模块（12个）

| 模块 | 功能 | 创新点 |
|------|------|--------|
| 🏠 首页仪表盘 | 数据概览、地图分布 | 古风UI设计 |
| 🌉 桥梁博览 | 31座古桥知识库 | 收藏筛选 |
| 📄 桥梁详情 | 完整信息展示 | 多维度信息 |
| ⏳ 时间轴 | 朝代演进历程 | 可视化时间线 |
| 🤖 AI问答 | GLM-4智能对话 | RAG知识库 |
| 🔬 结构剖析 | Three.js 3D模型 | 交互式3D |
| 👨‍🔧 匠心人物 | 建造者传记 | 工匠精神 |
| 🏗️ 古桥建造坊 | 拖拽建造模拟 | 游戏化学习 |
| ⚖️ 桥梁对比 | 多桥数据对比 | 可视化对比 |
| 🏆 知识挑战 | 答题闯关 | 徽章系统 |
| 📊 数据统计 | 多维数据分析 | 图表可视化 |
| ℹ️ 关于项目 | 项目介绍 | AI协同说明 |

## 🚀 快速开始

### 方式一：Docker 部署（推荐）

```bash
# 1. 克隆项目
git clone https://github.com/your-username/bridge-thousand-years.git
cd bridge-thousand-years

# 2. 配置环境变量
cp .env.example .env
# 编辑 .env，填入 GLM_API_KEY

# 3. 一键部署
./deploy.sh        # Linux/macOS
.\deploy.ps1       # Windows

# 4. 访问应用
# 前端: http://localhost
# 后端: http://localhost:5000
```

### 方式二：本地开发

```bash
# 前端
cd frontend
npm install
npm run dev     # http://localhost:5173

# 后端
cd backend
pip install -r requirements.txt
python run.py   # http://localhost:5000
```

## 🛠️ 技术栈

| 层级 | 技术 | 说明 |
|------|------|------|
| 前端框架 | Vue 3 | 组合式API |
| UI组件 | Element Plus | 企业级组件库 |
| 图表 | ECharts | 数据可视化 |
| 3D渲染 | Three.js | WebGL 3D模型 |
| 后端框架 | Flask | Python轻量框架 |
| 数据库 | SQLite | 轻量级数据库 |
| AI大模型 | GLM-4 | 智谱AI |

## 🤖 AI协同体现

本项目采用 **AI协同开发模式**，AI作为开发伙伴参与全程：

| AI工具 | 用途 | 占比 |
|--------|------|------|
| OpenClaw (Claude) | 架构设计、代码编写、文档生成 | 70% |
| GLM-4 | 智能问答功能 | 10% |
| GitHub Copilot | 代码辅助 | 5% |
| 人工优化 | UI调整、功能测试 | 15% |

### AI协同案例

1. **古风UI设计**：AI配色建议 + CSS代码生成
2. **数据可视化**：AI图表配置 + 交互优化
3. **移动端适配**：AI响应式CSS + 触摸优化

## 📁 项目结构

```
【桥见千年】/
├── frontend/           # 前端项目 (Vue 3)
│   ├── src/
│   │   ├── views/     # 12个页面组件
│   │   ├── components/
│   │   ├── api/
│   │   └── assets/
│   ├── Dockerfile
│   └── nginx.conf
│
├── backend/            # 后端项目 (Flask)
│   ├── app/
│   │   ├── routes/    # API路由
│   │   └── services/
│   ├── data/          # 桥梁数据
│   ├── Dockerfile
│   └── requirements.txt
│
├── docs/               # 文档
│   └── PROJECT_INTRODUCTION.md
│
├── docker-compose.yml  # Docker 编排
├── deploy.sh           # Linux 部署脚本
├── deploy.ps1          # Windows 部署脚本
└── README.md
```

## 📊 数据资源

收录 **31座** 中国古代著名桥梁：

- **拱桥**：赵州桥、卢沟桥、十七孔桥等
- **梁桥**：洛阳桥、广济桥、安平桥等
- **索桥**：泸定桥等

每座桥梁包含：基本信息、技术特点、建造者、历史文献、诗词典故等。

## 🎨 界面预览

### 古风UI设计

- **配色**：朱红 #8B2323 + 金色 #C9A962 + 米白 #F5F0E6
- **元素**：卷轴标题、印章标签、装饰角
- **风格**：传统文化与现代技术融合

### 响应式适配

- 桌面端完整布局
- 平板端双列布局
- 手机端单列布局

## 📝 环境配置

### 必需配置

```bash
# .env 文件
GLM_API_KEY=your_glm_api_key_here  # 智谱AI API Key
```

### 获取 API Key

1. 访问 [智谱AI开放平台](https://open.bigmodel.cn/)
2. 注册并登录
3. 创建 API Key

## 📖 文档

- [项目介绍文档](docs/PROJECT_INTRODUCTION.md)
- [Docker部署指南](docs/DOCKER_DEPLOY.md)

## 👥 团队

| 成员 | 角色 |
|------|------|
| 小宇 | 项目负责人、产品设计 |
| 小彩 (AI) | 开发工程师、架构师 |

## 📄 License

MIT License

## 🙏 致谢

- **智谱AI**：提供GLM-4大模型支持
- **Anthropic**：Claude AI协同开发
- **开源社区**：Vue、Element Plus、ECharts、Three.js

---

**项目口号**：桥见千年，连接古今 🌉
