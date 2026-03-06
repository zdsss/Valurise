import React, { Component, type ErrorInfo, type ReactNode } from 'react';

interface Props {
  children: ReactNode;
  fallback?: ReactNode;
}

interface State {
  hasError: boolean;
  error: Error | null;
  errorInfo: ErrorInfo | null;
}

class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = {
      hasError: false,
      error: null,
      errorInfo: null,
    };
  }

  static getDerivedStateFromError(error: Error): Partial<State> {
    return { hasError: true };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('ErrorBoundary caught an error:', error, errorInfo);
    this.setState({
      error,
      errorInfo,
    });

    // 这里可以集成错误监控服务（如Sentry）
    // Sentry.captureException(error, { extra: errorInfo });
  }

  handleReset = () => {
    this.setState({
      hasError: false,
      error: null,
      errorInfo: null,
    });
    window.location.href = '/';
  };

  render() {
    if (this.state.hasError) {
      // 如果提供了自定义fallback，使用它
      if (this.props.fallback) {
        return this.props.fallback;
      }

      // 默认错误UI
      return (
        <div className="min-h-screen flex items-center justify-center bg-gray-50 px-4">
          <div className="max-w-2xl w-full bg-white rounded-lg shadow-lg p-8">
            <div className="text-center mb-6">
              <div className="text-6xl mb-4">😵</div>
              <h1 className="text-3xl font-bold text-gray-900 mb-2">
                哎呀，出错了！
              </h1>
              <p className="text-gray-600">
                应用遇到了一个意外错误。我们已经记录了这个问题，会尽快修复。
              </p>
            </div>

            {import.meta.env.DEV && this.state.error && (
              <div className="mb-6">
                <details className="bg-red-50 border border-red-200 rounded-lg p-4">
                  <summary className="cursor-pointer font-medium text-red-900 mb-2">
                    错误详情（仅开发环境显示）
                  </summary>
                  <div className="mt-4 space-y-2">
                    <div>
                      <p className="font-semibold text-red-900">错误消息:</p>
                      <pre className="text-sm text-red-800 bg-red-100 p-2 rounded mt-1 overflow-auto">
                        {this.state.error.toString()}
                      </pre>
                    </div>
                    {this.state.errorInfo && (
                      <div>
                        <p className="font-semibold text-red-900">组件堆栈:</p>
                        <pre className="text-sm text-red-800 bg-red-100 p-2 rounded mt-1 overflow-auto max-h-64">
                          {this.state.errorInfo.componentStack}
                        </pre>
                      </div>
                    )}
                  </div>
                </details>
              </div>
            )}

            <div className="flex gap-4 justify-center">
              <button
                onClick={() => window.location.reload()}
                className="px-6 py-3 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition font-medium"
              >
                刷新页面
              </button>
              <button
                onClick={this.handleReset}
                className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition font-medium"
              >
                返回首页
              </button>
            </div>

            <div className="mt-6 text-center text-sm text-gray-500">
              <p>如果问题持续存在，请联系我们的支持团队。</p>
            </div>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;
