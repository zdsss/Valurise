"""
API package
导出所有路由
"""

from app.api import auth, analysis, payment, users

__all__ = ["auth", "analysis", "payment", "users"]
