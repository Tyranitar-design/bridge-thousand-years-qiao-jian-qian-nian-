# 贡献指南

感谢你对【桥见千年】项目的关注！欢迎参与贡献。

## 🤝 如何贡献

### 报告问题

如果你发现了Bug或有功能建议：

1. 查看 [Issues](../../issues) 确认问题未被报告
2. 创建新 Issue，包含：
   - 问题描述
   - 复现步骤
   - 期望行为
   - 实际行为
   - 截图（如有）

### 提交代码

1. **Fork 本仓库**

2. **克隆到本地**
   ```bash
   git clone https://github.com/your-username/bridge-thousand-years.git
   cd bridge-thousand-years
   ```

3. **创建分支**
   ```bash
   git checkout -b feature/your-feature-name
   ```

4. **进行修改**
   - 遵循代码风格
   - 添加必要的注释
   - 更新相关文档

5. **提交更改**
   ```bash
   git add .
   git commit -m "feat: 添加某某功能"
   ```

6. **推送到 GitHub**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **创建 Pull Request**

## 📝 提交信息规范

使用 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

- `feat:` 新功能
- `fix:` 修复Bug
- `docs:` 文档更新
- `style:` 代码格式（不影响功能）
- `refactor:` 重构
- `test:` 测试相关
- `chore:` 构建/工具相关

示例：
```
feat: 添加桥梁收藏功能
fix: 修复移动端显示问题
docs: 更新部署文档
```

## 🎨 代码风格

### 前端 (Vue)

- 使用 Vue 3 组合式 API
- 使用 `<script setup>` 语法
- 组件命名：PascalCase
- 文件命名：PascalCase.vue

### 后端 (Python)

- 遵循 PEP 8
- 使用类型注解
- 函数命名：snake_case

## 🌳 项目结构

```
frontend/
├── src/
│   ├── views/       # 页面组件
│   ├── components/  # 公共组件
│   ├── api/         # API接口
│   └── assets/      # 静态资源

backend/
├── app/
│   ├── routes/      # API路由
│   └── services/    # 业务逻辑
└── data/            # 数据文件
```

## ✅ 检查清单

提交 PR 前，请确认：

- [ ] 代码能正常运行
- [ ] 遵循代码风格规范
- [ ] 添加了必要的注释
- [ ] 更新了相关文档
- [ ] 提交信息符合规范

## 📞 联系方式

如有问题，可以：
- 创建 Issue
- 发送邮件至：[项目邮箱]

---

再次感谢你的贡献！🎉
