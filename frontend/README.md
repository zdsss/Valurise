# Valurise Frontend

AI驱动的职业价值发现平台 - 前端应用

## 技术栈

- **框架**: React 18 + TypeScript
- **构建工具**: Vite
- **样式**: TailwindCSS
- **路由**: React Router v6
- **状态管理**: Zustand
- **表单**: React Hook Form + Zod
- **HTTP客户端**: Axios

## 快速开始

### 1. 安装依赖

```bash
npm install
```

### 2. 配置环境变量

```bash
cp .env.example .env
```

### 3. 启动开发服务器

```bash
npm run dev
```

访问 http://localhost:5173

## 项目结构

```
src/
├── components/          # 可复用组件
├── pages/              # 页面组件
├── lib/                # 工具库
├── stores/             # Zustand状态管理
├── types/              # TypeScript类型定义
├── services/           # API服务
└── App.tsx             # 根组件
```

## 开发指南

详见项目文档。

---

**版本**: 1.0.0
