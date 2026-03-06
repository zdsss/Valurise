"""
应用配置管理
使用pydantic-settings管理环境变量
"""

from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """应用配置"""

    # App基础配置
    APP_NAME: str = "Valurise"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    # API配置
    API_V1_PREFIX: str = "/api/v1"

    # CORS配置
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "https://app.valurise.com"
    ]

    # 数据库配置
    DATABASE_URL: str

    # Redis配置
    REDIS_URL: str = "redis://localhost:6379/0"

    # JWT配置
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30

    # Anthropic API配置
    ANTHROPIC_API_KEY: str
    ANTHROPIC_BASE_URL: str | None = None
    MODEL_MAIN: str = "claude-sonnet-4-6"
    MODEL_FAST: str = "claude-haiku-4-6"

    # Stripe配置
    STRIPE_SECRET_KEY: str
    STRIPE_WEBHOOK_SECRET: str
    STRIPE_PRICE_BASIC: str = "price_basic"
    STRIPE_PRICE_PRO: str = "price_pro"
    STRIPE_PRICE_PREMIUM: str = "price_premium"

    # 成本配置
    TARGET_COST_PER_RUN: float = 0.50

    # Pydantic配置
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True
    )


# 创建全局配置实例
settings = Settings()
