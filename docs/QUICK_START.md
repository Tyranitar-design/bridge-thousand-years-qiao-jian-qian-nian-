# 快速开始指南

## 5分钟快速体验

### 方式一：在线演示（推荐）

访问在线演示地址：[待部署后填写]

### 方式二：本地运行

#### 1. 环境准备

确保你的电脑已安装：
- Node.js 18+ （[下载](https://nodejs.org/)）
- Python 3.9+ （[下载](https://www.python.org/)）

#### 2. 下载项目

```bash
git clone https://github.com/your-username/bridge-thousand-years.git
cd bridge-thousand-years
```

#### 3. 启动后端

```bash
cd backend

# 创建虚拟环境（可选）
python -m venv venv
source venv/bin/activate  # Linux/macOS
# 或 venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt

# 启动服务
python run.py
```

后端运行在 http://localhost:5000

#### 4. 启动前端

打开新终端：

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

前端运行在 http://localhost:5173

#### 5. 访问应用

浏览器打开 http://localhost:5173

---

## 功能演示路径

### 路径一：知识探索（5分钟）

1. **首页** - 查看数据概览和地图分布
2. **桥梁博览** - 浏览31座古桥，点击筛选
3. **桥梁详情** - 选择赵州桥，查看完整信息
4. **时间轴** - 了解桥梁发展历程

### 路径二：AI体验（3分钟）

1. **AI问答** - 点击左侧菜单「AI问答」
2. 输入问题：
   - "赵州桥为什么能屹立1400年不倒？"
   - "中国古代有哪些类型的桥梁？"
   - "敞肩拱技术是什么？"

### 路径三：互动体验（5分钟）

1. **结构剖析** - 3D模型交互，旋转查看
2. **古桥建造坊** - 拖拽组件，体验建造
3. **知识挑战** - 答题闯关，赢取徽章
4. **桥梁对比** - 选择赵州桥vs卢沟桥对比

### 路径四：数据洞察（3分钟）

1. **数据统计** - 查看多维度分析
2. **匠心人物** - 了解桥梁建造者

---

## 常见问题

### Q: 前端无法连接后端？

检查后端是否正常运行：
```bash
curl http://localhost:5000/api/bridges
```

### Q: AI问答不工作？

需要配置GLM API Key：
1. 访问 [智谱AI](https://open.bigmodel.cn/) 获取API Key
2. 在 `backend/.env` 中配置：
   ```
   GLM_API_KEY=your_api_key_here
   ```
3. 重启后端服务

### Q: 3D模型不显示？

确保浏览器支持WebGL，推荐使用Chrome/Firefox最新版本。

---

## 下一步

- 📖 阅读 [完整文档](docs/PROJECT_INTRODUCTION.md)
- 🐳 使用 [Docker部署](docs/DOCKER_DEPLOY.md)
- 🤝 参与 [贡献](CONTRIBUTING.md)

---

如有问题，欢迎提 [Issue](../../issues)！
