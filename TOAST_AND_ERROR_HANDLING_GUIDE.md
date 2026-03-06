# Toast通知和错误处理使用指南

**创建日期**: 2026年3月6日
**版本**: 1.0

---

## 📋 概述

本文档介绍如何在Valurise前端应用中使用Toast通知系统和改进的错误处理机制。

---

## 🎯 Toast通知系统

### 基本用法

Toast通知系统已经在App.tsx中全局配置，可以在任何组件中使用。

```typescript
import { useToast } from '../components/Toast';

function MyComponent() {
  const toast = useToast();

  const handleSuccess = () => {
    toast.success('操作成功！');
  };

  const handleError = () => {
    toast.error('操作失败，请重试');
  };

  const handleWarning = () => {
    toast.warning('请注意检查输入');
  };

  const handleInfo = () => {
    toast.info('这是一条提示信息');
  };

  return (
    <div>
      <button onClick={handleSuccess}>成功提示</button>
      <button onClick={handleError}>错误提示</button>
      <button onClick={handleWarning}>警告提示</button>
      <button onClick={handleInfo}>信息提示</button>
    </div>
  );
}
```

### 自定义持续时间

默认情况下，Toast会在5秒后自动消失。你可以自定义持续时间：

```typescript
// 3秒后消失
toast.success('操作成功', 3000);

// 10秒后消失
toast.error('这是一个重要错误', 10000);

// 不自动消失（传入0或负数）
toast.info('需要手动关闭', 0);
```

### API方法

```typescript
interface ToastAPI {
  // 显示成功消息
  success: (message: string, duration?: number) => void;

  // 显示错误消息
  error: (message: string, duration?: number) => void;

  // 显示警告消息
  warning: (message: string, duration?: number) => void;

  // 显示信息消息
  info: (message: string, duration?: number) => void;

  // 通用方法
  showToast: (type: 'success' | 'error' | 'warning' | 'info', message: string, duration?: number) => void;

  // 手动移除Toast
  removeToast: (id: string) => void;
}
```

---

## 🔧 错误处理

### API错误处理

API服务已经增强了错误处理，会自动将后端错误转换为友好的中文消息。

```typescript
import { apiClient, getErrorMessage } from '../services/api';
import { useToast } from '../components/Toast';

function MyComponent() {
  const toast = useToast();

  const handleSubmit = async () => {
    try {
      await apiClient.login({ email, password });
      toast.success('登录成功！');
    } catch (error) {
      // 使用getErrorMessage获取友好的错误消息
      const message = getErrorMessage(error);
      toast.error(message);
    }
  };
}
```

### 错误消息映射

系统已经预定义了常见错误的友好消息：

| 错误代码 | 友好消息 |
|---------|---------|
| INVALID_CREDENTIALS | 邮箱或密码错误，请重试 |
| USER_EXISTS | 该邮箱已被注册，请直接登录 |
| INSUFFICIENT_CREDITS | 积分不足，请先购买 |
| NETWORK_ERROR | 网络连接失败，请检查网络后重试 |
| SERVER_ERROR | 服务器错误，请稍后重试 |
| ... | ... |

完整列表见 `src/services/api.ts`

### 自定义错误处理

如果需要针对特定错误进行特殊处理：

```typescript
try {
  await apiClient.createAnalysis(data);
} catch (error: any) {
  // 检查特定错误代码
  if (error.response?.data?.error?.code === 'INSUFFICIENT_CREDITS') {
    toast.warning('积分不足，请先购买');
    navigate('/pricing');
    return;
  }

  // 使用默认错误处理
  toast.error(getErrorMessage(error));
}
```

---

## 💡 实际应用示例

### 示例1: 登录页面

```typescript
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { apiClient, getErrorMessage } from '../services/api';
import { useToast } from '../components/Toast';

export default function LoginPage() {
  const navigate = useNavigate();
  const toast = useToast();
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (data: LoginFormData) => {
    setIsSubmitting(true);
    try {
      await apiClient.login(data);
      toast.success('登录成功！');
      navigate('/dashboard');
    } catch (error) {
      toast.error(getErrorMessage(error));
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    // ... 表单UI
  );
}
```

### 示例2: 创建分析

```typescript
import { apiClient, getErrorMessage } from '../services/api';
import { useToast } from '../components/Toast';

export default function NewAnalysisPage() {
  const toast = useToast();

  const handleSubmit = async (data: AnalysisFormData) => {
    try {
      const response = await apiClient.createAnalysis(data);
      toast.success('分析已创建，正在处理中...');
      navigate(`/analysis/${response.analysis_id}/processing`);
    } catch (error: any) {
      // 特殊处理积分不足
      if (error.response?.data?.error?.code === 'INSUFFICIENT_CREDITS') {
        toast.warning('积分不足，请先购买积分');
        navigate('/pricing');
        return;
      }

      // 默认错误处理
      toast.error(getErrorMessage(error));
    }
  };

  return (
    // ... 表单UI
  );
}
```

### 示例3: 支付成功

```typescript
import { useEffect } from 'react';
import { apiClient, getErrorMessage } from '../services/api';
import { useToast } from '../components/Toast';

export default function PaymentSuccessPage() {
  const toast = useToast();

  useEffect(() => {
    const verifyPayment = async () => {
      try {
        await apiClient.verifyPayment(sessionId);
        toast.success('支付成功！积分已到账');
      } catch (error) {
        toast.error(getErrorMessage(error));
      }
    };

    verifyPayment();
  }, []);

  return (
    // ... UI
  );
}
```

---

## 🎨 Toast样式

Toast通知有4种类型，每种都有独特的视觉样式：

### Success（成功）
- 背景：绿色
- 图标：✓
- 用途：操作成功、保存成功等

### Error（错误）
- 背景：红色
- 图标：✕
- 用途：操作失败、验证错误等

### Warning（警告）
- 背景：黄色
- 图标：⚠
- 用途：需要注意的信息、警告提示等

### Info（信息）
- 背景：蓝色
- 图标：ℹ
- 用途：一般信息、提示等

---

## 🔍 调试技巧

### 查看错误详情

在开发环境中，可以在控制台查看完整的错误对象：

```typescript
try {
  await apiClient.someMethod();
} catch (error) {
  console.error('API Error:', error);
  toast.error(getErrorMessage(error));
}
```

### 测试Toast

可以在浏览器控制台直接测试Toast：

```javascript
// 在任何页面的控制台执行
window.testToast = () => {
  const event = new CustomEvent('show-toast', {
    detail: { type: 'success', message: '测试消息' }
  });
  window.dispatchEvent(event);
};
```

---

## 📝 最佳实践

### 1. 使用合适的Toast类型

```typescript
// ✅ 好的做法
toast.success('保存成功');
toast.error('保存失败');
toast.warning('请先填写必填项');
toast.info('正在处理中...');

// ❌ 不好的做法
toast.info('保存失败'); // 应该用error
toast.success('请注意'); // 应该用warning
```

### 2. 消息要简洁明了

```typescript
// ✅ 好的做法
toast.success('登录成功');
toast.error('邮箱格式不正确');

// ❌ 不好的做法
toast.success('您已经成功登录到系统，现在可以使用所有功能了');
toast.error('您输入的邮箱地址格式不符合标准的邮箱格式要求');
```

### 3. 避免重复显示

```typescript
// ✅ 好的做法
const [isSubmitting, setIsSubmitting] = useState(false);

const handleSubmit = async () => {
  if (isSubmitting) return; // 防止重复提交
  setIsSubmitting(true);
  try {
    await apiClient.submit();
    toast.success('提交成功');
  } catch (error) {
    toast.error(getErrorMessage(error));
  } finally {
    setIsSubmitting(false);
  }
};
```

### 4. 错误处理要全面

```typescript
// ✅ 好的做法
try {
  await apiClient.someMethod();
  toast.success('操作成功');
} catch (error) {
  toast.error(getErrorMessage(error));
} finally {
  setIsLoading(false); // 确保清理状态
}

// ❌ 不好的做法
try {
  await apiClient.someMethod();
  toast.success('操作成功');
} catch (error) {
  // 没有错误提示，用户不知道发生了什么
}
```

---

## 🚀 高级用法

### 组合使用Loading和Toast

```typescript
import Loading from '../components/Loading';
import { useToast } from '../components/Toast';

function MyComponent() {
  const toast = useToast();
  const [isLoading, setIsLoading] = useState(false);

  const handleAction = async () => {
    setIsLoading(true);
    try {
      await apiClient.someMethod();
      toast.success('操作成功');
    } catch (error) {
      toast.error(getErrorMessage(error));
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoading) {
    return <Loading fullScreen text="处理中..." />;
  }

  return (
    // ... UI
  );
}
```

### 链式操作

```typescript
const handleMultiStep = async () => {
  try {
    // 步骤1
    await step1();
    toast.info('步骤1完成');

    // 步骤2
    await step2();
    toast.info('步骤2完成');

    // 步骤3
    await step3();
    toast.success('所有步骤完成！');
  } catch (error) {
    toast.error(getErrorMessage(error));
  }
};
```

---

## 📚 相关文档

- `src/components/Toast.tsx` - Toast组件实现
- `src/services/api.ts` - API错误处理
- `P0_P1_IMPROVEMENTS_REPORT.md` - 改进实施报告

---

**更新日期**: 2026年3月6日
**版本**: 1.0
