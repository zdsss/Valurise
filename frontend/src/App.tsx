import { useEffect } from 'react';
import { RouterProvider } from 'react-router-dom';
import { router } from './lib/router';
import { useAuthStore } from './stores/authStore';

function App() {
  const fetchCurrentUser = useAuthStore((state) => state.fetchCurrentUser);

  useEffect(() => {
    // 应用启动时尝试获取当前用户信息
    fetchCurrentUser();
  }, [fetchCurrentUser]);

  return <RouterProvider router={router} />;
}

export default App;
