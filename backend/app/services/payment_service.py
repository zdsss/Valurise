"""
支付服务
Stripe集成
"""

import stripe
from typing import Dict, Any
from app.config import settings

# 配置Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY


class PaymentService:
    """支付服务类"""

    # 定价配置
    PRICING = {
        "basic": {
            "name": "基础版",
            "price_cents": 4900,  # $49
            "credits": 1,
            "stripe_price_id": settings.STRIPE_PRICE_BASIC
        },
        "pro": {
            "name": "专业版",
            "price_cents": 9900,  # $99
            "credits": 1,
            "stripe_price_id": settings.STRIPE_PRICE_PRO
        },
        "premium": {
            "name": "高级版",
            "price_cents": 19900,  # $199
            "credits": 2,
            "stripe_price_id": settings.STRIPE_PRICE_PREMIUM
        }
    }

    @classmethod
    def create_checkout_session(
        cls,
        product_tier: str,
        user_id: str,
        success_url: str,
        cancel_url: str
    ) -> Dict[str, Any]:
        """
        创建Stripe Checkout会话

        Args:
            product_tier: 产品层级（basic/pro/premium）
            user_id: 用户ID
            success_url: 成功回调URL
            cancel_url: 取消回调URL

        Returns:
            包含session_id和checkout_url的字典

        Raises:
            ValueError: 无效的产品层级
            stripe.error.StripeError: Stripe API错误
        """
        if product_tier not in cls.PRICING:
            raise ValueError(f"无效的产品层级: {product_tier}")

        pricing = cls.PRICING[product_tier]

        try:
            # 创建Checkout会话
            session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=[
                    {
                        "price": pricing["stripe_price_id"],
                        "quantity": 1,
                    }
                ],
                mode="payment",
                success_url=success_url,
                cancel_url=cancel_url,
                client_reference_id=user_id,
                metadata={
                    "user_id": user_id,
                    "product_tier": product_tier,
                    "credits": pricing["credits"]
                }
            )

            return {
                "session_id": session.id,
                "checkout_url": session.url
            }

        except stripe.error.StripeError as e:
            raise e

    @classmethod
    def verify_webhook_signature(
        cls,
        payload: bytes,
        signature: str
    ) -> Dict[str, Any]:
        """
        验证Stripe Webhook签名

        Args:
            payload: 请求体（bytes）
            signature: Stripe-Signature头

        Returns:
            Stripe事件对象

        Raises:
            stripe.error.SignatureVerificationError: 签名验证失败
        """
        try:
            event = stripe.Webhook.construct_event(
                payload,
                signature,
                settings.STRIPE_WEBHOOK_SECRET
            )
            return event
        except stripe.error.SignatureVerificationError as e:
            raise e

    @classmethod
    def get_session(cls, session_id: str) -> Dict[str, Any]:
        """
        获取Checkout会话信息

        Args:
            session_id: 会话ID

        Returns:
            会话信息字典

        Raises:
            stripe.error.StripeError: Stripe API错误
        """
        try:
            session = stripe.checkout.Session.retrieve(session_id)
            return {
                "id": session.id,
                "payment_status": session.payment_status,
                "payment_intent": session.payment_intent,
                "amount_total": session.amount_total,
                "currency": session.currency,
                "customer_email": session.customer_details.email if session.customer_details else None,
                "metadata": session.metadata
            }
        except stripe.error.StripeError as e:
            raise e

    @classmethod
    def get_pricing_info(cls, product_tier: str) -> Dict[str, Any]:
        """
        获取定价信息

        Args:
            product_tier: 产品层级

        Returns:
            定价信息字典

        Raises:
            ValueError: 无效的产品层级
        """
        if product_tier not in cls.PRICING:
            raise ValueError(f"无效的产品层级: {product_tier}")

        return cls.PRICING[product_tier]


# 创建全局支付服务实例
payment_service = PaymentService()
