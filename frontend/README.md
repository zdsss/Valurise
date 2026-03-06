# Valurise Frontend

AI驱动的职业价值发现平台 - 前端应用

## ✅ 开发状态

**当前版本**: v1.0.0
**完成度**: 100%
**最后更新**: 2026年3月6日

### 已完成功能

- ✅ 用户认证（登录/注册）
- ✅ 用户Dashboard
- ✅ 职业信息输入表单
- ✅ 实时分析进度展示
- ✅ 分析结果展示（4个Agent结果）
- ✅ 定价页面
- ✅ Stripe支付集成
- ✅ 响应式设计
- ✅ 路由保护
- ✅ 错误处理

## 技术栈

- **框架**: React 19 + TypeScript
- **构建工具**: Vite 7
- **样式**: TailwindCSS 3
- **路由**: React Router v7
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

编辑 `.env` 文件：
```
VITE_API_URL=http://localhost:8000/api/v1
```

### 3. 启动开发服务器

```bash
npm run dev
```

访问 http://localhost:5173

### 4. 构建生产版本

```bash
npm run build
```

构建产物在 `dist/` 目录

## 项目结构

```
src/
├── components/
│   └── layouts/         # 布局组件
│       ├── RootLayout.tsx
│       └── AuthLayout.tsx
├── pages/               # 页面组件
│   ├── HomePage.tsx
│   ├── LoginPage.tsx
│   ├── RegisterPage.tsx
│   ├── DashboardPage.tsx
│   ├── NewAnalysisPage.tsx
│   ├── AnalysisProcessingPage.tsx
│   ├── AnalysisResultPage.tsx
│   ├── PricingPage.tsx
│   ├── PaymentSuccessPage.tsx
│   └── PaymentCancelPage.tsx
├── lib/
│   └── router.tsx       # 路由配置
├── stores/
│   └── authStore.ts     # 认证状态管理
├── services/
│   └── api.ts           # API客户端
├── types/
│   └── index.ts         # TypeScript类型
├── App.tsx
├── main.tsx
└── index.css
```

## 核心功能

### 1. 用户认证
- 注册新用户
- 登录/登出
- JWT Token管理
- 自动刷新Token

### 2. 分析流程
1. 用户输入职业信息（NewAnalysisPage）
2. 提交后跳转到进度页面（AnalysisProcessingPage）
3. 实时轮询显示4个Agent的处理进度
4. 完成后自动跳转到结果页面（AnalysisResultPage）

### 3. 结果展示
- 信息提取结果
- 价值分析报告
- 叙事策略
- 优化简历

### 4. 支付集成
- Stripe Checkout集成
- 支付成功/取消页面
- 自动验证支付状态

## API集成

所有API调用通过 `src/services/api.ts` 中的 `apiClient` 进行：

```typescript
// 示例
import { apiClient } from './services/api';

// 登录
await apiClient.login({ email, password });

// 创建分析
await apiClient.createAnalysis({ raw_input, target_role });

// 获取分析状态
await apiClient.getAnalysisStatus(analysisId);
```

## 状态管理

使用Zustand进行状态管理，目前只有认证状态：

```typescript
import { useAuthStore } from './stores/authStore';

const { user, isAuthenticated, login, logout } = useAuthStore();
```

## 路由保护

受保护的路由需要用户登录才能访问：

- `/dashboard` - 用户Dashboard
- `/analysis/new` - 新建分析
- `/analysis/:id/processing` - 分析进度
- `/analysis/:id/result` - 分析结果
- `/payment/*` - 支付相关

## 开发注意事项

### TypeScript配置
- 已禁用严格模式以加快开发速度
- 生产环境建议启用严格模式

### Tailwind CSS
- 使用v3版本（兼容Node 18）
- 自定义颜色和样式在 `index.css` 中定义

### 环境要求
- Node.js 18+ （推荐20+）
- npm 10+

## 部署

### Vercel部署（推荐）

1. 连接GitHub仓库
2. 设置环境变量：
   - `VITE_API_URL`: 后端API地址
3. 自动部署

### 手动部署

```bash
npm run build
# 将 dist/ 目录部署到静态服务器
```

## 性能优化

- ✅ 代码分割（React Router）
- ✅ 懒加载组件
- ✅ 生产构建优化
- ✅ Gzip压缩

## 浏览器支持

- Chrome (最新)
- Firefox (最新)
- Safari (最新)
- Edge (最新)

---

**版本**: 1.0.0
**团队**: Valurise开发团队
**更新**: 2026年3月6日
