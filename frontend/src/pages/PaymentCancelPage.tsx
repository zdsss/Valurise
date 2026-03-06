import { useNavigate } from 'react-router-dom';

export default function PaymentCancelPage() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="bg-white p-8 rounded-lg shadow-lg text-center max-w-md">
        <div className="text-yellow-600 text-6xl mb-4">⚠</div>
        <h2 className="text-3xl font-bold mb-4">支付已取消</h2>
        <p className="text-gray-600 mb-6">
          您已取消支付流程。如果遇到问题，请联系客服或重新尝试。
        </p>
        <div className="space-y-3">
          <button
            onClick={() => navigate('/pricing')}
            className="w-full px-6 py-3 bg-blue-600 text-white rounded hover:bg-blue-700 font-medium"
          >
            返回定价页
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
