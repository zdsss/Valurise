import { useEffect, useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { apiClient } from '../services/api';

export default function PaymentSuccessPage() {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const [isVerifying, setIsVerifying] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const sessionId = searchParams.get('session_id');
    if (!sessionId) {
      setError('缺少支付会话ID');
      setIsVerifying(false);
      return;
    }

    const verifyPayment = async () => {
      try {
        await apiClient.verifyPayment(sessionId);
        setIsVerifying(false);
      } catch (err: any) {
        setError(err.response?.data?.error?.message || '验证支付失败');
        setIsVerifying(false);
      }
    };

    verifyPayment();
  }, [searchParams]);

  if (isVerifying) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="bg-white p-8 rounded-lg shadow-lg text-center max-w-md">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <h2 className="text-2xl font-bold mb-2">验证支付中...</h2>
          <p className="text-gray-600">请稍候，正在确认您的支付</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="bg-white p-8 rounded-lg shadow-lg text-center max-w-md">
          <div className="text-red-600 text-6xl mb-4">✕</div>
          <h2 className="text-2xl font-bold mb-4">支付验证失败</h2>
          <p className="text-gray-600 mb-6">{error}</p>
          <div className="flex gap-4 justify-center">
            <button
              onClick={() => navigate('/pricing')}
              className="px-6 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
            >
              返回定价页
            </button>
            <button
              onClick={() => navigate('/dashboard')}
              className="px-6 py-2 border border-gray-300 rounded hover:bg-gray-50"
            >
              返回首页
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="bg-white p-8 rounded-lg shadow-lg text-center max-w-md">
        <div className="text-green-600 text-6xl mb-4">✓</div>
        <h2 className="text-3xl font-bold mb-4">支付成功！</h2>
        <p className="text-gray-600 mb-6">
          感谢您的购买！您现在可以开始使用职业价值分析服务了。
        </p>
        <div className="space-y-3">
          <button
            onClick={() => navigate('/analysis/new')}
            className="w-full px-6 py-3 bg-blue-600 text-white rounded hover:bg-blue-700 font-medium"
          >
            开始分析
          </button>
          <button
            onClick={() => navigate('/dashboard')}
            className="w-full px-6 py-3 border border-gray-300 rounded hover:bg-gray-50"
          >
            返回首页
          </button>
        </div>
      </div>
    </div>
  );
}
