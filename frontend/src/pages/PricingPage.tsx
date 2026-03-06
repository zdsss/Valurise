import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuthStore } from '../stores/authStore';
import { apiClient } from '../services/api';

const pricingPlans = [
  {
    id: 'basic',
    name: '基础版',
    price: 49,
    description: '适合个人求职者',
    features: [
      '1次完整职业价值分析',
      '信息提取与结构化',
      '价值分析与技能识别',
      '职业叙事策略',
      '优化简历生成',
      '7天结果保存',
    ],
    recommended: false,
  },
  {
    id: 'professional',
    name: '专业版',
    price: 99,
    description: '适合职业转型者',
    features: [
      '3次完整职业价值分析',
      '所有基础版功能',
      '多版本简历生成',
      '行业对比分析',
      '30天结果保存',
      '优先处理',
    ],
    recommended: true,
  },
  {
    id: 'premium',
    name: '高级版',
    price: 199,
    description: '适合高级管理者',
    features: [
      '10次完整职业价值分析',
      '所有专业版功能',
      '深度能力图谱',
      '竞争力分析报告',
      '永久结果保存',
      '专属客服支持',
    ],
    recommended: false,
  },
];

export default function PricingPage() {
  const navigate = useNavigate();
  const { isAuthenticated } = useAuthStore();
  const [isProcessing, setIsProcessing] = useState<string | null>(null);

  const handleSelectPlan = async (planId: string) => {
    if (!isAuthenticated) {
      navigate('/login');
      return;
    }

    setIsProcessing(planId);
    try {
      const response = await apiClient.createCheckout({
        price_id: planId,
        success_url: `${window.location.origin}/payment/success?session_id={CHECKOUT_SESSION_ID}`,
        cancel_url: `${window.location.origin}/payment/cancel`,
      });

      // 跳转到Stripe Checkout
      window.location.href = response.checkout_url;
    } catch (err: any) {
      alert(err.response?.data?.error?.message || '创建支付会话失败');
      setIsProcessing(null);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-16">
      <div className="container mx-auto px-4">
        <div className="max-w-6xl mx-auto">
          {/* 头部 */}
          <div className="text-center mb-12">
            <h1 className="text-4xl md:text-5xl font-bold mb-4">选择适合你的方案</h1>
            <p className="text-xl text-gray-600">
              所有方案都包含完整的AI职业价值分析功能
            </p>
          </div>

          {/* 定价卡片 */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-12">
            {pricingPlans.map((plan) => (
              <div
                key={plan.id}
                className={`bg-white rounded-lg shadow-lg overflow-hidden ${
                  plan.recommended ? 'ring-2 ring-blue-600 transform scale-105' : ''
                }`}
              >
                {plan.recommended && (
                  <div className="bg-blue-600 text-white text-center py-2 font-medium">
                    推荐方案
                  </div>
                )}
                <div className="p-8">
                  <h3 className="text-2xl font-bold mb-2">{plan.name}</h3>
                  <p className="text-gray-600 mb-6">{plan.description}</p>
                  <div className="mb-6">
                    <span className="text-5xl font-bold">${plan.price}</span>
                    <span className="text-gray-600 ml-2">/ 次</span>
                  </div>
                  <button
                    onClick={() => handleSelectPlan(plan.id)}
                    disabled={isProcessing === plan.id}
                    className={`w-full py-3 rounded-lg font-medium transition ${
                      plan.recommended
                        ? 'bg-blue-600 text-white hover:bg-blue-700'
                        : 'bg-gray-100 text-gray-900 hover:bg-gray-200'
                    } disabled:opacity-50 disabled:cursor-not-allowed`}
                  >
                    {isProcessing === plan.id ? '处理中...' : '选择方案'}
                  </button>
                  <ul className="mt-8 space-y-4">
                    {plan.features.map((feature, idx) => (
                      <li key={idx} className="flex items-start">
                        <svg
                          className="w-5 h-5 text-green-600 mr-3 flex-shrink-0 mt-0.5"
                          fill="none"
                          stroke="currentColor"
                          viewBox="0 0 24 24"
                        >
                          <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            strokeWidth={2}
                            d="M5 13l4 4L19 7"
                          />
                        </svg>
                        <span className="text-gray-700">{feature}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            ))}
          </div>

          {/* FAQ */}
          <div className="bg-white rounded-lg shadow-lg p-8">
            <h2 className="text-2xl font-bold mb-6">常见问题</h2>
            <div className="space-y-6">
              <div>
                <h3 className="font-medium text-lg mb-2">分析需要多长时间？</h3>
                <p className="text-gray-600">
                  通常需要2-4分钟完成完整的分析流程，包括信息提取、价值分析、叙事策略和简历优化。
                </p>
              </div>
              <div>
                <h3 className="font-medium text-lg mb-2">可以退款吗？</h3>
                <p className="text-gray-600">
                  如果您对分析结果不满意，可以在7天内申请全额退款。
                </p>
              </div>
              <div>
                <h3 className="font-medium text-lg mb-2">支持哪些支付方式？</h3>
                <p className="text-gray-600">
                  我们通过Stripe支持信用卡、借记卡等多种支付方式。
                </p>
              </div>
              <div>
                <h3 className="font-medium text-lg mb-2">数据安全吗？</h3>
                <p className="text-gray-600">
                  我们使用行业标准的加密技术保护您的数据，不会与第三方分享您的个人信息。
                </p>
              </div>
            </div>
          </div>

          {/* CTA */}
          <div className="mt-12 text-center">
            <p className="text-gray-600 mb-4">还有疑问？</p>
            <button
              onClick={() => navigate('/')}
              className="text-blue-600 hover:underline font-medium"
            >
              返回首页了解更多
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
