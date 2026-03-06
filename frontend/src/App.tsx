import { useEffect } from 'react';
import { RouterProvider } from 'react-router-dom';
import { router } from './lib/router';
import { useAuthStore } from './stores/authStore';
import ErrorBoundary from './components/ErrorBoundary';
import { ToastProvider } from './components/Toast';

function App() {
  const fetchCurrentUser = useAuthStore((state) => state.fetchCurrentUser);

  useEffect(() => {
    // 应用启动时尝试获取当前用户信息
    fetchCurrentUser();
  }, [fetchCurrentUser]);

  return (
    <ErrorBoundary>
      <ToastProvider>
        <RouterProvider router={router} />
      </ToastProvider>
    </ErrorBoundary>
  );
}

export default App;
