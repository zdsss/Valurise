import { createBrowserRouter, Navigate } from 'react-router-dom';
import { lazy, Suspense } from 'react';
import { useAuthStore } from '../stores/authStore';
import Loading from '../components/Loading';

// Layouts (不懒加载，因为是核心布局)
import RootLayout from '../components/layouts/RootLayout';
import AuthLayout from '../components/layouts/AuthLayout';

// 懒加载页面组件
const HomePage = lazy(() => import('../pages/HomePage'));
const LoginPage = lazy(() => import('../pages/LoginPage'));
const RegisterPage = lazy(() => import('../pages/RegisterPage'));
const DashboardPage = lazy(() => import('../pages/DashboardPage'));
const NewAnalysisPage = lazy(() => import('../pages/NewAnalysisPage'));
const AnalysisProcessingPage = lazy(() => import('../pages/AnalysisProcessingPage'));
const AnalysisResultPage = lazy(() => import('../pages/AnalysisResultPage'));
const PricingPage = lazy(() => import('../pages/PricingPage'));
const PaymentSuccessPage = lazy(() => import('../pages/PaymentSuccessPage'));
const PaymentCancelPage = lazy(() => import('../pages/PaymentCancelPage'));
const NotFoundPage = lazy(() => import('../pages/NotFoundPage'));

// Suspense包装器
function SuspenseWrapper({ children }: { children: React.ReactNode }) {
  return (
    <Suspense fallback={<Loading fullScreen text="加载中..." />}>
      {children}
    </Suspense>
  );
}

// Protected Route Component
function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated);

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return <>{children}</>;
}

export const router = createBrowserRouter([
  {
    path: '/',
    element: <RootLayout />,
    children: [
      {
        index: true,
        element: (
          <SuspenseWrapper>
            <HomePage />
          </SuspenseWrapper>
        ),
      },
      {
        path: 'pricing',
        element: (
          <SuspenseWrapper>
            <PricingPage />
          </SuspenseWrapper>
        ),
      },
      {
        path: 'dashboard',
        element: (
          <ProtectedRoute>
            <SuspenseWrapper>
              <DashboardPage />
            </SuspenseWrapper>
          </ProtectedRoute>
        ),
      },
      {
        path: 'analysis/new',
        element: (
          <ProtectedRoute>
            <SuspenseWrapper>
              <NewAnalysisPage />
            </SuspenseWrapper>
          </ProtectedRoute>
        ),
      },
      {
        path: 'analysis/:analysisId/processing',
        element: (
          <ProtectedRoute>
            <SuspenseWrapper>
              <AnalysisProcessingPage />
            </SuspenseWrapper>
          </ProtectedRoute>
        ),
      },
      {
        path: 'analysis/:analysisId/result',
        element: (
          <ProtectedRoute>
            <SuspenseWrapper>
              <AnalysisResultPage />
            </SuspenseWrapper>
          </ProtectedRoute>
        ),
      },
      {
        path: 'payment/success',
        element: (
          <ProtectedRoute>
            <SuspenseWrapper>
              <PaymentSuccessPage />
            </SuspenseWrapper>
          </ProtectedRoute>
        ),
      },
      {
        path: 'payment/cancel',
        element: (
          <ProtectedRoute>
            <SuspenseWrapper>
              <PaymentCancelPage />
            </SuspenseWrapper>
          </ProtectedRoute>
        ),
      },
      {
        path: '*',
        element: (
          <SuspenseWrapper>
            <NotFoundPage />
          </SuspenseWrapper>
        ),
      },
    ],
  },
  {
    element: <AuthLayout />,
    children: [
      {
        path: 'login',
        element: (
          <SuspenseWrapper>
            <LoginPage />
          </SuspenseWrapper>
        ),
      },
      {
        path: 'register',
        element: (
          <SuspenseWrapper>
            <RegisterPage />
          </SuspenseWrapper>
        ),
      },
    ],
  },
]);
