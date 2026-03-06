import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { useNavigate } from 'react-router-dom';
import { apiClient } from '../services/api';

const analysisSchema = z.object({
  raw_input: z.string().min(100, '请至少输入100个字符，详细描述您的职业经历'),
  target_role: z.string().min(2, '请输入目标岗位'),
  target_industry: z.string().optional(),
});

type AnalysisFormData = z.infer<typeof analysisSchema>;

export default function NewAnalysisPage() {
  const navigate = useNavigate();
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const {
    register,
    handleSubmit,
    watch,
    formState: { errors },
  } = useForm<AnalysisFormData>({
    resolver: zodResolver(analysisSchema),
  });

  const rawInput = watch('raw_input', '');
  const charCount = rawInput.length;

  const onSubmit = async (data: AnalysisFormData) => {
    setIsSubmitting(true);
    setError(null);
    try {
      const response = await apiClient.createAnalysis(data);
      navigate(`/analysis/${response.analysis_id}/processing`);
    } catch (err: any) {
      setError(err.response?.data?.error?.message || '创建分析失败，请重试');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="container mx-auto px-4 py-8 max-w-4xl">
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-2">开始职业价值分析</h1>
        <p className="text-gray-600">
          请详细描述您的职业经历、技能和成就，我们的AI将帮您深度挖掘职业价值
        </p>
      </div>

      {error && (
        <div className="mb-6 p-4 bg-red-50 border border-red-200 text-red-700 rounded">
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
        {/* 职业经历输入 */}
        <div className="bg-white p-6 rounded-lg shadow">
          <label htmlFor="raw_input" className="block text-lg font-medium mb-2">
            职业经历描述 *
          </label>
          <p className="text-sm text-gray-600 mb-4">
            请详细描述您的工作经历、项目经验、技能特长、主要成就等。内容越详细，分析结果越准确。
          </p>
          <textarea
            id="raw_input"
            {...register('raw_input')}
            rows={12}
            className="w-full px-4 py-3 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="例如：&#10;&#10;我在过去5年担任产品经理，主导了3个从0到1的产品项目...&#10;&#10;- 项目A：用户增长从0到50万，月活跃率达到65%&#10;- 项目B：带领8人团队，成功完成产品转型&#10;- 核心技能：用户研究、数据分析、敏捷开发&#10;&#10;请尽可能详细地描述您的经历和成就。"
          />
          <div className="mt-2 flex justify-between items-center">
            <div>
              {errors.raw_input && (
                <p className="text-sm text-red-600">{errors.raw_input.message}</p>
              )}
            </div>
            <p className={`text-sm ${charCount < 100 ? 'text-red-600' : 'text-gray-500'}`}>
              {charCount} / 100 字符（最少）
            </p>
          </div>
        </div>

        {/* 目标岗位 */}
        <div className="bg-white p-6 rounded-lg shadow">
          <label htmlFor="target_role" className="block text-lg font-medium mb-2">
            目标岗位 *
          </label>
          <p className="text-sm text-gray-600 mb-4">
            您希望应聘的岗位名称，例如：高级产品经理、技术总监、市场营销经理等
          </p>
          <input
            id="target_role"
            type="text"
            {...register('target_role')}
            className="w-full px-4 py-3 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="例如：高级产品经理"
          />
          {errors.target_role && (
            <p className="mt-2 text-sm text-red-600">{errors.target_role.message}</p>
          )}
        </div>

        {/* 目标行业（可选） */}
        <div className="bg-white p-6 rounded-lg shadow">
          <label htmlFor="target_industry" className="block text-lg font-medium mb-2">
            目标行业（可选）
          </label>
          <p className="text-sm text-gray-600 mb-4">
            您希望进入的行业，例如：互联网、金融、教育、医疗等
          </p>
          <input
            id="target_industry"
            type="text"
            {...register('target_industry')}
            className="w-full px-4 py-3 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="例如：互联网"
          />
        </div>

        {/* 提交按钮 */}
        <div className="flex justify-between items-center pt-4">
          <button
            type="button"
            onClick={() => navigate('/dashboard')}
            className="px-6 py-3 border border-gray-300 rounded hover:bg-gray-50 transition"
          >
            取消
          </button>
          <button
            type="submit"
            disabled={isSubmitting || charCount < 100}
            className="px-8 py-3 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition"
          >
            {isSubmitting ? '提交中...' : '开始分析'}
          </button>
        </div>
      </form>

      {/* 说明信息 */}
      <div className="mt-8 p-6 bg-blue-50 border border-blue-200 rounded-lg">
        <h3 className="font-medium mb-2">💡 温馨提示</h3>
        <ul className="text-sm text-gray-700 space-y-1">
          <li>• 分析过程大约需要 2-4 分钟</li>
          <li>• 您可以随时查看分析进度</li>
          <li>• 分析完成后会生成详细的职业价值报告和优化简历</li>
          <li>• 所有数据都会安全保存，您可以随时查看历史记录</li>
        </ul>
      </div>
    </div>
  );
}
