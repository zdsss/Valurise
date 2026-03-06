import { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuthStore } from '../stores/authStore';
import { apiClient } from '../services/api';
import type { AnalysisHistoryItem } from '../types';

export default function DashboardPage() {
  const { user, logout } = useAuthStore();
  const navigate = useNavigate();
  const [analyses, setAnalyses] = useState<AnalysisHistoryItem[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchAnalyses = async () => {
      try {
        const data = await apiClient.getAnalysisHistory(1, 10);
        setAnalyses(data.analyses);
      } catch (err) {
        console.error('Failed to fetch analyses:', err);
      } finally {
        setIsLoading(false);
      }
    };

    fetchAnalyses();
  }, []);

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  const getStatusBadge = (status: string) => {
    const badges: Record<string, { bg: string; text: string; label: string }> = {
      pending: { bg: 'bg-gray-100', text: 'text-gray-700', label: '等待中' },
      processing: { bg: 'bg-blue-100', text: 'text-blue-700', label: '处理中' },
      completed: { bg: 'bg-green-100', text: 'text-green-700', label: '已完成' },
      failed: { bg: 'bg-red-100', text: 'text-red-700', label: '失败' },
    };
    const badge = badges[status] || badges.pending;
    return (
      <span className={`px-2 py-1 rounded text-sm ${badge.bg} ${badge.text}`}>
        {badge.label}
      </span>
    );
  };

  return (
    <div className="container mx-auto px-4 py-8 max-w-6xl">
      {/* 头部 */}
      <div className="bg-white p-6 rounded-lg shadow mb-6">
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-bold mb-2">欢迎回来，{user?.full_name || user?.email}</h1>
            <p className="text-gray-600">管理您的职业价值分析</p>
          </div>
          <button
            onClick={handleLogout}
            className="px-4 py-2 border border-gray-300 rounded hover:bg-gray-50"
          >
            退出登录
          </button>
        </div>
      </div>

      {/* 快速操作 */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <Link
          to="/analysis/new"
          className="p-6 bg-blue-600 text-white rounded-lg shadow hover:bg-blue-700 transition"
        >
          <div className="text-4xl mb-2">✨</div>
          <h3 className="text-xl font-bold mb-1">开始新分析</h3>
          <p className="text-blue-100">创建新的职业价值分析</p>
        </Link>

        <Link
          to="/pricing"
          className="p-6 bg-white border-2 border-gray-200 rounded-lg shadow hover:border-blue-500 transition"
        >
          <div className="text-4xl mb-2">💳</div>
          <h3 className="text-xl font-bold mb-1">查看定价</h3>
          <p className="text-gray-600">了解我们的服务套餐</p>
        </Link>

        <div className="p-6 bg-white border-2 border-gray-200 rounded-lg shadow">
          <div className="text-4xl mb-2">📊</div>
          <h3 className="text-xl font-bold mb-1">分析统计</h3>
          <p className="text-gray-600">已完成 {analyses.filter(a => a.status === 'completed').length} 次分析</p>
        </div>
      </div>

      {/* 分析历史 */}
      <div className="bg-white rounded-lg shadow">
        <div className="p-6 border-b border-gray-200">
          <h2 className="text-2xl font-bold">我的分析</h2>
        </div>

        {isLoading ? (
          <div className="p-8 text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
            <p className="text-gray-600">加载中...</p>
          </div>
        ) : analyses.length === 0 ? (
          <div className="p-8 text-center">
            <div className="text-gray-400 text-5xl mb-4">📋</div>
            <h3 className="text-xl font-medium mb-2">还没有分析记录</h3>
            <p className="text-gray-600 mb-6">开始您的第一次职业价值分析吧！</p>
            <Link
              to="/analysis/new"
              className="inline-block px-6 py-3 bg-blue-600 text-white rounded hover:bg-blue-700"
            >
              开始分析
            </Link>
          </div>
        ) : (
          <div className="divide-y divide-gray-200">
            {analyses.map((analysis) => (
              <div key={analysis.id} className="p-6 hover:bg-gray-50 transition">
                <div className="flex justify-between items-start">
                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-2">
                      <h3 className="text-lg font-medium">{analysis.target_role}</h3>
                      {getStatusBadge(analysis.status)}
                    </div>
                    {analysis.target_industry && (
                      <p className="text-sm text-gray-600 mb-2">
                        目标行业: {analysis.target_industry}
                      </p>
                    )}
                    <p className="text-sm text-gray-500">
                      创建时间: {new Date(analysis.created_at).toLocaleString('zh-CN')}
                    </p>
                    {analysis.completed_at && (
                      <p className="text-sm text-gray-500">
                        完成时间: {new Date(analysis.completed_at).toLocaleString('zh-CN')}
                      </p>
                    )}
                  </div>

                  <div className="flex gap-2">
                    {analysis.status === 'processing' && (
                      <Link
                        to={`/analysis/${analysis.id}/processing`}
                        className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
                      >
                        查看进度
                      </Link>
                    )}
                    {analysis.status === 'completed' && (
                      <Link
                        to={`/analysis/${analysis.id}/result`}
                        className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700"
                      >
                        查看结果
                      </Link>
                    )}
                    {analysis.status === 'failed' && (
                      <button
                        onClick={() => navigate('/analysis/new')}
                        className="px-4 py-2 bg-gray-600 text-white rounded hover:bg-gray-700"
                      >
                        重新分析
                      </button>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
