import { Outlet, Link } from 'react-router-dom';
import { useAuthStore } from '../../stores/authStore';

export default function RootLayout() {
  const { isAuthenticated, user, logout } = useAuthStore();

  return (
    <div className="min-h-screen flex flex-col">
      {/* Header */}
      <header className="border-b">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <Link to="/" className="text-2xl font-bold text-primary">
            Valurise
          </Link>

          <nav className="flex items-center gap-6">
            {isAuthenticated ? (
              <>
                <Link to="/dashboard" className="text-sm font-medium hover:text-primary">
                  Dashboard
                </Link>
                <Link to="/analysis/new" className="text-sm font-medium hover:text-primary">
                  新建分析
                </Link>
                <div className="flex items-center gap-4">
                  <span className="text-sm text-muted-foreground">
                    {user?.email}
                  </span>
                  <span className="text-sm font-medium">
                    积分: {user?.credits_remaining || 0}
                  </span>
                  <button
                    onClick={logout}
                    className="text-sm font-medium text-destructive hover:underline"
                  >
                    退出
                  </button>
                </div>
              </>
            ) : (
              <>
                <Link to="/pricing" className="text-sm font-medium hover:text-primary">
                  定价
                </Link>
                <Link to="/login" className="text-sm font-medium hover:text-primary">
                  登录
                </Link>
                <Link
                  to="/register"
                  className="px-4 py-2 bg-primary text-primary-foreground rounded-md text-sm font-medium hover:bg-primary/90"
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
      <footer className="border-t py-6 mt-auto">
        <div className="container mx-auto px-4 text-center text-sm text-muted-foreground">
          © 2026 Valurise. All rights reserved.
        </div>
      </footer>
    </div>
  );
}
