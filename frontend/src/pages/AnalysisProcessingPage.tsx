import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { apiClient } from '../services/api';
import type { AnalysisStatus } from '../types';

export default function AnalysisProcessingPage() {
  const { analysisId } = useParams<{ analysisId: string }>();
  const navigate = useNavigate();
  const [status, setStatus] = useState<AnalysisStatus | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!analysisId) {
      navigate('/dashboard');
      return;
    }

    let intervalId: ReturnType<typeof setInterval>;

    const fetchStatus = async () => {
      try {
        const data = await apiClient.getAnalysisStatus(analysisId);
        setStatus(data);

        // 如果完成或失败，跳转到结果页面
        if (data.status === 'completed') {
          clearInterval(intervalId);
          setTimeout(() => {
            navigate(`/analysis/${analysisId}/result`);
          }, 1000);
        } else if (data.status === 'failed') {
          clearInterval(intervalId);
          setError(data.error_message || '分析失败');
        }
      } catch (err: any) {
        setError(err.response?.data?.error?.message || '获取状态失败');
        clearInterval(intervalId);
      }
    };

    // 立即获取一次
    fetchStatus();

    // 每3秒轮询一次
    intervalId = setInterval(fetchStatus, 3000);

    return () => {
      if (intervalId) clearInterval(intervalId);
    };
  }, [analysisId, navigate]);

  const getProgressPercentage = () => {
    if (!status) return 0;
    if (status.status === 'completed') return 100;
    if (status.status === 'failed') return 0;

    // 根据当前步骤计算进度
    const stepProgress: Record<string, number> = {
      'pending': 0,
      'extracting': 25,
      'analyzing': 50,
      'strategizing': 75,
      'optimizing': 90,
      'processing': 10,
    };

    return stepProgress[status.current_step] || 10;
  };

  const getStepLabel = (step: string) => {
    const labels: Record<string, string> = {
      'pending': '准备中',
      'extracting': '提取职业信息',
      'analyzing': '分析职业价值',
      'strategizing': '构建叙事策略',
      'optimizing': '优化简历',
      'processing': '处理中',
      'completed': '完成',
      'failed': '失败',
    };
    return labels[step] || step;
  };

  if (error) {
    return (
      <div className="container mx-auto px-4 py-8 max-w-2xl">
        <div className="bg-white p-8 rounded-lg shadow text-center">
          <div className="text-red-600 text-5xl mb-4">✕</div>
          <h2 className="text-2xl font-bold mb-4">分析失败</h2>
          <p className="text-gray-600 mb-6">{error}</p>
          <button
            onClick={() => navigate('/dashboard')}
            className="px-6 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
          >
            返回首页
          </button>
        </div>
      </div>
    );
  }

  if (!status) {
    return (
      <div className="container mx-auto px-4 py-8 max-w-2xl">
        <div className="bg-white p-8 rounded-lg shadow text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">加载中...</p>
        </div>
      </div>
    );
  }

  const progress = getProgressPercentage();

  return (
    <div className="container mx-auto px-4 py-8 max-w-2xl">
      <div className="bg-white p-8 rounded-lg shadow">
        <h1 className="text-3xl font-bold mb-2 text-center">正在分析您的职业价值</h1>
        <p className="text-gray-600 text-center mb-8">
          请稍候，AI正在深度分析您的职业经历...
        </p>

        {/* 进度条 */}
        <div className="mb-8">
          <div className="flex justify-between mb-2">
            <span className="text-sm font-medium text-gray-700">
              {getStepLabel(status.current_step)}
            </span>
            <span className="text-sm font-medium text-gray-700">{progress}%</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-3">
            <div
              className="bg-blue-600 h-3 rounded-full transition-all duration-500"
              style={{ width: `${progress}%` }}
            ></div>
          </div>
        </div>

        {/* 步骤指示器 */}
        <div className="space-y-4">
          {[
            { key: 'extracting', label: '提取职业信息', icon: '📋' },
            { key: 'analyzing', label: '分析职业价值', icon: '💎' },
            { key: 'strategizing', label: '构建叙事策略', icon: '📖' },
            { key: 'optimizing', label: '优化简历', icon: '✨' },
          ].map((step, index) => {
            const isActive = status.current_step === step.key;
            const isCompleted = progress > (index + 1) * 25;

            return (
              <div
                key={step.key}
                className={`flex items-center p-4 rounded-lg border-2 transition ${
                  isActive
                    ? 'border-blue-500 bg-blue-50'
                    : isCompleted
                    ? 'border-green-500 bg-green-50'
                    : 'border-gray-200 bg-gray-50'
                }`}
              >
                <div className="text-3xl mr-4">{step.icon}</div>
                <div className="flex-1">
                  <h3 className="font-medium">{step.label}</h3>
                </div>
                {isCompleted && <div className="text-green-600 text-xl">✓</div>}
                {isActive && (
                  <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-blue-600"></div>
                )}
              </div>
            );
          })}
        </div>

        {/* 统计信息 */}
        {status.stats && (
          <div className="mt-8 p-4 bg-gray-50 rounded-lg">
            <h3 className="font-medium mb-2">处理统计</h3>
            <div className="grid grid-cols-2 gap-4 text-sm">
              <div>
                <span className="text-gray-600">已用时间：</span>
                <span className="font-medium ml-2">
                  {Math.round((status.stats.elapsed_time || 0))}秒
                </span>
              </div>
              <div>
                <span className="text-gray-600">预计剩余：</span>
                <span className="font-medium ml-2">
                  {Math.round((status.stats.estimated_remaining_time || 0))}秒
                </span>
              </div>
            </div>
          </div>
        )}

        {/* 提示信息 */}
        <div className="mt-8 p-4 bg-blue-50 border border-blue-200 rounded-lg">
          <p className="text-sm text-gray-700">
            💡 分析过程通常需要 2-4 分钟，请保持页面打开。您也可以关闭页面，稍后在"我的分析"中查看结果。
          </p>
        </div>
      </div>
    </div>
  );
}
