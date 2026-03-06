"""
支付相关API
Stripe支付集成
"""

from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Request, Header
from sqlalchemy.orm import Session
import stripe

from app.database import get_db
from app.models.user import User
from app.models.order import Order
from app.schemas.order import (
    CreateCheckoutRequest,
    CreateCheckoutResponse,
    PaymentVerifyResponse,
    WebhookResponse
)
from app.api.deps import get_current_active_user
from app.services.payment_service import payment_service

router = APIRouter()


@router.post("/create-checkout", response_model=CreateCheckoutResponse)
async def create_checkout_session(
    checkout_data: CreateCheckoutRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    创建Stripe支付会话

    - **product_tier**: 产品层级（basic/pro/premium）
    - **success_url**: 支付成功回调URL
    - **cancel_url**: 支付取消回调URL

    返回checkout_session_id和checkout_url
    """
    try:
        # 获取定价信息
        pricing = payment_service.get_pricing_info(checkout_data.product_tier)

        # 创建订单记录
        new_order = Order(
            user_id=current_user.id,
            product_tier=checkout_data.product_tier,
            amount_cents=pricing["price_cents"],
            currency="USD",
            status="pending"
        )

        db.add(new_order)
        db.commit()
        db.refresh(new_order)

        # 创建Stripe Checkout会话
        session_data = payment_service.create_checkout_session(
            product_tier=checkout_data.product_tier,
            user_id=str(current_user.id),
            success_url=str(checkout_data.success_url),
            cancel_url=str(checkout_data.cancel_url)
        )

        # 更新订单的session_id
        new_order.stripe_checkout_session_id = session_data["session_id"]
        db.commit()

        return CreateCheckoutResponse(
            checkout_session_id=session_data["session_id"],
            checkout_url=session_data["checkout_url"],
            order_id=new_order.id
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e)
        )
    except stripe.error.StripeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Stripe错误: {str(e)}"
        )


@router.post("/webhook", response_model=WebhookResponse)
async def stripe_webhook(
    request: Request,
    stripe_signature: str = Header(None, alias="stripe-signature"),
    db: Session = Depends(get_db)
):
    """
    Stripe Webhook处理

    处理支付成功、失败等事件
    """
    if not stripe_signature:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="缺少Stripe签名"
        )

    # 获取请求体
    payload = await request.body()

    try:
        # 验证签名
        event = payment_service.verify_webhook_signature(payload, stripe_signature)

        # 处理事件
        if event["type"] == "checkout.session.completed":
            # 支付成功
            session = event["data"]["object"]
            await _handle_checkout_completed(session, db)

        elif event["type"] == "payment_intent.succeeded":
            # 支付确认
            payment_intent = event["data"]["object"]
            print(f"Payment intent succeeded: {payment_intent['id']}")

        elif event["type"] == "payment_intent.payment_failed":
            # 支付失败
            payment_intent = event["data"]["object"]
            await _handle_payment_failed(payment_intent, db)

        return WebhookResponse(received=True)

    except stripe.error.SignatureVerificationError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="无效的Stripe签名"
        )
    except Exception as e:
        print(f"Webhook处理错误: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Webhook处理失败: {str(e)}"
        )


@router.get("/verify/{session_id}", response_model=PaymentVerifyResponse)
async def verify_payment(
    session_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    验证支付状态

    - **session_id**: Stripe Checkout会话ID

    返回订单状态和支付信息
    """
    # 查询订单
    order = db.query(Order).filter(
        Order.stripe_checkout_session_id == session_id,
        Order.user_id == current_user.id
    ).first()

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="订单不存在"
        )

    return PaymentVerifyResponse(
        order_id=order.id,
        status=order.status,
        product_tier=order.product_tier,
        amount_cents=order.amount_cents,
        paid_at=order.paid_at,
        analysis_id=order.analysis_id
    )


async def _handle_checkout_completed(session: dict, db: Session):
    """
    处理支付成功事件

    Args:
        session: Stripe会话对象
        db: 数据库会话
    """
    session_id = session["id"]
    payment_intent_id = session.get("payment_intent")
    metadata = session.get("metadata", {})

    # 查询订单
    order = db.query(Order).filter(
        Order.stripe_checkout_session_id == session_id
    ).first()

    if not order:
        print(f"订单不存在: {session_id}")
        return

    # 更新订单状态
    order.status = "paid"
    order.stripe_payment_intent_id = payment_intent_id
    order.paid_at = datetime.utcnow()

    # 增加用户积分
    user = db.query(User).filter(User.id == order.user_id).first()
    if user:
        credits = int(metadata.get("credits", 1))
        user.credits_remaining += credits

        # 更新订阅层级
        product_tier = metadata.get("product_tier")
        if product_tier:
            user.subscription_tier = product_tier

    db.commit()

    print(f"支付成功处理完成: {session_id}")


async def _handle_payment_failed(payment_intent: dict, db: Session):
    """
    处理支付失败事件

    Args:
        payment_intent: Stripe支付意图对象
        db: 数据库会话
    """
    payment_intent_id = payment_intent["id"]

    # 查询订单
    order = db.query(Order).filter(
        Order.stripe_payment_intent_id == payment_intent_id
    ).first()

    if not order:
        print(f"订单不存在: {payment_intent_id}")
        return

    # 更新订单状态
    order.status = "failed"
    db.commit()

    print(f"支付失败处理完成: {payment_intent_id}")
