import { Link } from 'react-router-dom';

export default function NotFoundPage() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 px-4">
      <div className="max-w-md w-full text-center">
        <div className="mb-8">
          <h1 className="text-9xl font-bold text-blue-600">404</h1>
          <div className="text-6xl mb-4">🔍</div>
          <h2 className="text-3xl font-bold text-gray-900 mb-2">页面未找到</h2>
          <p className="text-gray-600 mb-8">
            抱歉，您访问的页面不存在或已被移除。
          </p>
        </div>

        <div className="space-y-4">
          <Link
            to="/"
            className="block w-full px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition font-medium"
          >
            返回首页
          </Link>
          <Link
            to="/dashboard"
            className="block w-full px-6 py-3 border-2 border-gray-300 text-gray-700 rounded-lg hover:border-blue-500 hover:text-blue-600 transition font-medium"
          >
            前往Dashboard
          </Link>
        </div>

        <div className="mt-8 text-sm text-gray-500">
          <p>如果您认为这是一个错误，请联系我们的支持团队。</p>
        </div>
      </div>
    </div>
  );
}
