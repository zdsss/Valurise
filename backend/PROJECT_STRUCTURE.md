# FastAPI后端项目结构

backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI应用入口
│   ├── config.py               # 配置管理
│   ├── database.py             # 数据库连接
│   │
│   ├── models/                 # SQLAlchemy模型
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── analysis.py
│   │   └── order.py
│   │
│   ├── schemas/                # Pydantic schemas
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── analysis.py
│   │   └── order.py
│   │
│   ├── api/                    # API路由
│   │   ├── __init__.py
│   │   ├── deps.py            # 依赖项
│   │   ├── auth.py            # 认证相关
│   │   ├── analysis.py        # 分析相关
│   │   ├── payment.py         # 支付相关
│   │   └── users.py           # 用户相关
│   │
│   ├── core/                   # 核心功能
│   │   ├── __init__.py
│   │   ├── security.py        # JWT、密码哈希
│   │   └── celery_app.py      # Celery配置
│   │
│   └── services/               # 业务逻辑
│       ├── __init__.py
│       ├── agent_service.py   # Agent服务
│       └── payment_service.py # 支付服务
│
├── agents_optimized.py         # 优化后的Agent（已完成）
├── test_optimized_agents.py    # Agent测试（已完成）
├── requirements.txt            # Python依赖
├── .env                        # 环境变量
├── .env.example                # 环境变量示例
└── README.md                   # 项目说明
