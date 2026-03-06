# 📐 Valurise 技术规范文档

**版本**: v1.0
**更新日期**: 2026年3月10日
**状态**: Draft

---

## 🎯 概述

本文档定义Valurise Web应用的技术规范，包括API设计、数据模型、认证方案等。

---

## 🗄️ 数据库设计

### 表结构

#### 1. users 表

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    is_verified BOOLEAN DEFAULT FALSE,
    subscription_tier VARCHAR(20) DEFAULT 'free',
    -- free, basic, pro, premium
    credits_remaining INT DEFAULT 0
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_created_at ON users(created_at);
```

#### 2. analyses 表

```sql
CREATE TABLE analyses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    -- pending, processing, completed, failed

    -- 输入数据
    input_data JSONB NOT NULL,
    target_role JSONB NOT NULL,

    -- 输出数据
    extracted_info JSONB,
    value_analysis JSONB,
    narrative_strategy JSONB,
    resume_versions JSONB,

    -- 元数据
    cost DECIMAL(10, 4),
    processing_time_seconds INT,
    error_message TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,

    CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE INDEX idx_analyses_user_id ON analyses(user_id);
CREATE INDEX idx_analyses_status ON analyses(status);
CREATE INDEX idx_analyses_created_at ON analyses(created_at);
```

#### 3. orders 表

```sql
CREATE TABLE orders (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    analysis_id UUID REFERENCES analyses(id) ON DELETE SET NULL,

    -- Stripe相关
    stripe_checkout_session_id VARCHAR(255) UNIQUE,
    stripe_payment_intent_id VARCHAR(255),

    -- 订单信息
    product_tier VARCHAR(20) NOT NULL,
    -- basic, pro, premium
    amount_cents INT NOT NULL,
    currency VARCHAR(3) DEFAULT 'USD',
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    -- pending, paid, failed, refunded

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    paid_at TIMESTAMP,

    CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users(id),
    CONSTRAINT fk_analysis FOREIGN KEY (analysis_id) REFERENCES analyses(id)
);

CREATE INDEX idx_orders_user_id ON orders(user_id);
CREATE INDEX idx_orders_stripe_session ON orders(stripe_checkout_session_id);
CREATE INDEX idx_orders_status ON orders(status);
```

#### 4. api_logs 表（可选，用于监控）

```sql
CREATE TABLE api_logs (
    id BIGSERIAL PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    endpoint VARCHAR(255) NOT NULL,
    method VARCHAR(10) NOT NULL,
    status_code INT NOT NULL,
    response_time_ms INT,
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_api_logs_user_id ON api_logs(user_id);
CREATE INDEX idx_api_logs_created_at ON api_logs(created_at);
CREATE INDEX idx_api_logs_endpoint ON api_logs(endpoint);
```

---

## 🔌 API设计

### 基础信息

**Base URL**: `https://api.valurise.com/v1`
**认证方式**: JWT Bearer Token
**Content-Type**: `application/json`

### 认证相关 API

#### POST /auth/register

注册新用户

**Request**:
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123!",
  "full_name": "张三"
}
```

**Response** (201):
```json
{
  "user": {
    "id": "uuid",
    "email": "user@example.com",
    "full_name": "张三",
    "created_at": "2026-03-10T10:00:00Z"
  },
  "access_token": "eyJ...",
  "token_type": "bearer"
}
```

**Errors**:
- 400: Email already exists
- 422: Validation error

---

#### POST /auth/login

用户登录

**Request**:
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123!"
}
```

**Response** (200):
```json
{
  "user": {
    "id": "uuid",
    "email": "user@example.com",
    "full_name": "张三",
    "subscription_tier": "free",
    "credits_remaining": 0
  },
  "access_token": "eyJ...",
  "token_type": "bearer"
}
```

**Errors**:
- 401: Invalid credentials
- 404: User not found

---

#### POST /auth/refresh

刷新访问令牌

**Headers**:
```
Authorization: Bearer <refresh_token>
```

**Response** (200):
```json
{
  "access_token": "eyJ...",
  "token_type": "bearer"
}
```

---

### 分析相关 API

#### POST /analyses

创建新的分析任务

**Headers**:
```
Authorization: Bearer <access_token>
```

**Request**:
```json
{
  "input_data": {
    "raw_text": "我叫张伟，有5年的产品经理经验...",
    "work_experiences": [
      {
        "company": "某互联网公司",
        "position": "高级产品经理",
        "start_date": "2021-01",
        "end_date": "present",
        "responsibilities": ["负责AI助手产品线..."],
        "achievements": ["用户量从0增长到50万"]
      }
    ],
    "education": [
      {
        "institution": "北京大学",
        "degree": "学士",
        "field": "计算机科学",
        "graduation_date": "2019"
      }
    ],
    "skills": ["产品设计", "用户研究", "数据分析"]
  },
  "target_role": {
    "title": "AI产品总监",
    "industry": "人工智能/互联网",
    "key_requirements": ["5年以上产品经验", "AI产品经验"]
  },
  "options": {
    "num_resume_versions": 1,
    "include_linkedin": false
  }
}
```

**Response** (202):
```json
{
  "analysis_id": "uuid",
  "status": "pending",
  "estimated_time_seconds": 120,
  "created_at": "2026-03-10T10:00:00Z"
}
```

**Errors**:
- 401: Unauthorized
- 402: Payment required (no credits)
- 422: Validation error

---

#### GET /analyses/{analysis_id}

获取分析状态

**Headers**:
```
Authorization: Bearer <access_token>
```

**Response** (200):
```json
{
  "id": "uuid",
  "status": "processing",
  "progress": {
    "current_step": 2,
    "total_steps": 4,
    "current_agent": "value_analysis",
    "message": "正在分析职业价值..."
  },
  "created_at": "2026-03-10T10:00:00Z",
  "started_at": "2026-03-10T10:00:05Z",
  "estimated_completion": "2026-03-10T10:02:05Z"
}
```

**Status值**:
- `pending`: 等待处理
- `processing`: 处理中
- `completed`: 已完成
- `failed`: 失败

---

#### GET /analyses/{analysis_id}/result

获取分析结果

**Headers**:
```
Authorization: Bearer <access_token>
```

**Response** (200):
```json
{
  "id": "uuid",
  "status": "completed",
  "result": {
    "extracted_info": {
      "structured_profile": {...},
      "missing_info": [...],
      "raw_insights": [...]
    },
    "value_analysis": {
      "key_achievements": [...],
      "transferable_skills": [...],
      "unique_value_props": [...],
      "hidden_strengths": [...],
      "capability_map": {...}
    },
    "narrative_strategy": {
      "career_narrative": "...",
      "story_arcs": [...],
      "positioning_statement": "...",
      "key_messages": [...],
      "differentiation_points": [...]
    },
    "resume_versions": [
      {
        "target_role": "...",
        "summary": "...",
        "work_experiences": [...],
        "skills_section": {...},
        "education": [...],
        "ats_keywords": [...],
        "optimization_notes": [...]
      }
    ]
  },
  "metadata": {
    "cost": 0.17,
    "processing_time_seconds": 115,
    "completed_at": "2026-03-10T10:02:00Z"
  }
}
```

**Errors**:
- 404: Analysis not found
- 403: Not authorized to access this analysis
- 425: Analysis not completed yet

---

#### GET /analyses

获取用户的分析历史

**Headers**:
```
Authorization: Bearer <access_token>
```

**Query Parameters**:
- `page`: 页码（默认1）
- `limit`: 每页数量（默认10，最大50）
- `status`: 过滤状态（可选）

**Response** (200):
```json
{
  "analyses": [
    {
      "id": "uuid",
      "status": "completed",
      "target_role": "AI产品总监",
      "created_at": "2026-03-10T10:00:00Z",
      "completed_at": "2026-03-10T10:02:00Z",
      "cost": 0.17
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 10,
    "total": 5,
    "total_pages": 1
  }
}
```

---

### 支付相关 API

#### POST /payment/create-checkout

创建Stripe支付会话

**Headers**:
```
Authorization: Bearer <access_token>
```

**Request**:
```json
{
  "product_tier": "pro",
  "success_url": "https://app.valurise.com/payment/success?session_id={CHECKOUT_SESSION_ID}",
  "cancel_url": "https://app.valurise.com/payment/cancel"
}
```

**Response** (200):
```json
{
  "checkout_session_id": "cs_test_...",
  "checkout_url": "https://checkout.stripe.com/c/pay/cs_test_...",
  "order_id": "uuid"
}
```

**Errors**:
- 401: Unauthorized
- 422: Invalid product tier

---

#### POST /payment/webhook

Stripe Webhook处理

**Headers**:
```
Stripe-Signature: t=...,v1=...
```

**Request**: Stripe Event Object

**Response** (200):
```json
{
  "received": true
}
```

**处理的事件**:
- `checkout.session.completed`: 支付成功
- `payment_intent.succeeded`: 支付确认
- `payment_intent.payment_failed`: 支付失败

---

#### GET /payment/verify/{session_id}

验证支付状态

**Headers**:
```
Authorization: Bearer <access_token>
```

**Response** (200):
```json
{
  "order_id": "uuid",
  "status": "paid",
  "product_tier": "pro",
  "amount_cents": 9900,
  "paid_at": "2026-03-10T10:05:00Z",
  "analysis_id": "uuid"
}
```

---

### 用户相关 API

#### GET /users/me

获取当前用户信息

**Headers**:
```
Authorization: Bearer <access_token>
```

**Response** (200):
```json
{
  "id": "uuid",
  "email": "user@example.com",
  "full_name": "张三",
  "subscription_tier": "pro",
  "credits_remaining": 1,
  "created_at": "2026-03-10T10:00:00Z",
  "stats": {
    "total_analyses": 3,
    "completed_analyses": 2,
    "total_spent_cents": 9900
  }
}
```

---

#### PATCH /users/me

更新用户信息

**Headers**:
```
Authorization: Bearer <access_token>
```

**Request**:
```json
{
  "full_name": "张三丰"
}
```

**Response** (200):
```json
{
  "id": "uuid",
  "email": "user@example.com",
  "full_name": "张三丰",
  "updated_at": "2026-03-10T10:10:00Z"
}
```

---

## 🔐 认证方案

### JWT Token结构

**Access Token** (有效期: 1小时):
```json
{
  "sub": "user_id",
  "email": "user@example.com",
  "type": "access",
  "exp": 1234567890,
  "iat": 1234567890
}
```

**Refresh Token** (有效期: 30天):
```json
{
  "sub": "user_id",
  "type": "refresh",
  "exp": 1234567890,
  "iat": 1234567890
}
```

### 密码要求

- 最小长度: 8字符
- 必须包含: 大写字母、小写字母、数字
- 推荐包含: 特殊字符

### 密码哈希

使用 `bcrypt` 算法，cost factor = 12

---

## 📡 WebSocket (可选，用于实时进度)

### 连接

```
wss://api.valurise.com/v1/ws/analysis/{analysis_id}?token=<access_token>
```

### 消息格式

**服务器 → 客户端**:
```json
{
  "type": "progress",
  "data": {
    "current_step": 2,
    "total_steps": 4,
    "current_agent": "value_analysis",
    "message": "正在分析职业价值...",
    "progress_percentage": 50
  }
}
```

```json
{
  "type": "completed",
  "data": {
    "analysis_id": "uuid",
    "status": "completed"
  }
}
```

```json
{
  "type": "error",
  "data": {
    "message": "处理失败，请重试"
  }
}
```

---

## 🔄 错误处理

### 标准错误响应

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": {
      "field": "email",
      "issue": "Invalid email format"
    }
  }
}
```

### 错误代码

| HTTP Status | Error Code | Description |
|-------------|------------|-------------|
| 400 | BAD_REQUEST | 请求格式错误 |
| 401 | UNAUTHORIZED | 未认证 |
| 402 | PAYMENT_REQUIRED | 需要付费 |
| 403 | FORBIDDEN | 无权限访问 |
| 404 | NOT_FOUND | 资源不存在 |
| 422 | VALIDATION_ERROR | 数据验证失败 |
| 425 | TOO_EARLY | 资源尚未准备好 |
| 429 | RATE_LIMIT_EXCEEDED | 请求过于频繁 |
| 500 | INTERNAL_ERROR | 服务器内部错误 |
| 503 | SERVICE_UNAVAILABLE | 服务暂时不可用 |

---

## 🚦 速率限制

### 限制规则

**未认证用户**:
- 10 requests / minute

**已认证用户**:
- 60 requests / minute
- 10 analysis creations / hour

**响应头**:
```
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 45
X-RateLimit-Reset: 1234567890
```

**超限响应** (429):
```json
{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Too many requests",
    "retry_after": 60
  }
}
```

---

## 📊 数据验证

### 输入数据验证

**Email**:
- 格式: RFC 5322
- 最大长度: 255字符

**Password**:
- 最小长度: 8字符
- 最大长度: 128字符
- 必须包含: 大小写字母、数字

**工作经历**:
- 公司名称: 1-100字符
- 职位: 1-100字符
- 日期格式: YYYY-MM 或 "present"

**目标岗位**:
- 标题: 1-100字符
- 行业: 1-100字符
- 关键要求: 数组，每项1-200字符

---

## 🔒 安全措施

### HTTPS

所有API必须通过HTTPS访问

### CORS

```python
CORS_ORIGINS = [
    "https://app.valurise.com",
    "http://localhost:3000",  # 开发环境
]
```

### SQL注入防护

使用ORM（SQLAlchemy）参数化查询

### XSS防护

- 输入验证
- 输出转义
- Content-Security-Policy头

### CSRF防护

- SameSite Cookie
- CSRF Token（如使用Cookie认证）

---

## 📈 性能优化

### 数据库索引

已在表结构中定义关键索引

### 缓存策略

**Redis缓存**:
- 用户信息: TTL 5分钟
- 分析结果: TTL 1小时
- API响应: TTL 1分钟（GET请求）

### 分页

默认分页大小: 10
最大分页大小: 50

---

## 🧪 测试

### API测试

使用 `pytest` + `httpx`

**示例**:
```python
def test_create_analysis(client, auth_token):
    response = client.post(
        "/v1/analyses",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={
            "input_data": {...},
            "target_role": {...}
        }
    )
    assert response.status_code == 202
    assert "analysis_id" in response.json()
```

### 集成测试

测试完整的用户流程:
1. 注册 → 登录
2. 创建分析 → 等待完成
3. 获取结果 → 验证数据

---

## 📝 API文档

### 自动生成

使用FastAPI自动生成OpenAPI文档

**访问地址**:
- Swagger UI: `https://api.valurise.com/docs`
- ReDoc: `https://api.valurise.com/redoc`
- OpenAPI JSON: `https://api.valurise.com/openapi.json`

---

## 🔄 版本控制

### API版本

当前版本: `v1`

URL格式: `https://api.valurise.com/v1/...`

### 版本策略

- 向后兼容的更改: 不增加版本号
- 破坏性更改: 增加版本号（v2, v3...）
- 旧版本支持: 至少6个月

---

## 📞 支持

### 技术支持

- Email: dev@valurise.com
- 文档: https://docs.valurise.com
- GitHub: https://github.com/valurise/api

---

**文档版本**: v1.0
**最后更新**: 2026年3月10日
**下次审查**: 2026年4月1日
