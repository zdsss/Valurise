import { Outlet, Link, useNavigate } from 'react-router-dom';
import { useAuthStore } from '../../stores/authStore';

export default function RootLayout() {
  const { isAuthenticated, user, logout } = useAuthStore();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  return (
    <div className="min-h-screen flex flex-col">
      {/* Header */}
      <header className="border-b bg-white shadow-sm">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <Link to="/" className="text-2xl font-bold text-blue-600 hover:text-blue-700">
            Valurise
          </Link>

          <nav className="flex items-center gap-6">
            {isAuthenticated ? (
              <>
                <Link to="/dashboard" className="text-sm font-medium hover:text-blue-600">
                  我的分析
                </Link>
                <Link to="/analysis/new" className="text-sm font-medium hover:text-blue-600">
                  新建分析
                </Link>
                <Link to="/pricing" className="text-sm font-medium hover:text-blue-600">
                  定价
                </Link>
                <div className="flex items-center gap-4 pl-4 border-l">
                  <span className="text-sm text-gray-600">
                    {user?.full_name || user?.email}
                  </span>
                  <span className="text-sm font-medium bg-blue-100 text-blue-700 px-2 py-1 rounded">
                    积分: {user?.credits_remaining || 0}
                  </span>
                  <button
                    onClick={handleLogout}
                    className="text-sm font-medium text-red-600 hover:underline"
                  >
                    退出
                  </button>
                </div>
              </>
            ) : (
              <>
                <Link to="/pricing" className="text-sm font-medium hover:text-blue-600">
                  定价
                </Link>
                <Link to="/login" className="text-sm font-medium hover:text-blue-600">
                  登录
                </Link>
                <Link
                  to="/register"
                  className="px-4 py-2 bg-blue-600 text-white rounded-md text-sm font-medium hover:bg-blue-700"
                >
                  注册
                </Link>
              </>
            )}
          </nav>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1">
        <Outlet />
      </main>

      {/* Footer */}
      <footer className="border-t py-8 mt-auto bg-gray-50">
        <div className="container mx-auto px-4">
          <div className="flex justify-between items-center">
            <div>
              <p className="text-sm text-gray-600">© 2026 Valurise. All rights reserved.</p>
            </div>
            <div className="flex gap-6">
              <Link to="/" className="text-sm text-gray-600 hover:text-blue-600">
                关于我们
              </Link>
              <Link to="/pricing" className="text-sm text-gray-600 hover:text-blue-600">
                定价
              </Link>
              <a href="mailto:support@valurise.com" className="text-sm text-gray-600 hover:text-blue-600">
                联系我们
              </a>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}
