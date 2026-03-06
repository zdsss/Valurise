import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { apiClient } from '../services/api';
import type { AnalysisResultResponse } from '../types';

export default function AnalysisResultPage() {
  const { analysisId } = useParams<{ analysisId: string }>();
  const navigate = useNavigate();
  const [result, setResult] = useState<AnalysisResultResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<'extraction' | 'analysis' | 'narrative' | 'resume'>('extraction');

  useEffect(() => {
    if (!analysisId) {
      navigate('/dashboard');
      return;
    }

    const fetchResult = async () => {
      try {
        const data = await apiClient.getAnalysisResult(analysisId);
        setResult(data);
      } catch (err: any) {
        setError(err.response?.data?.error?.message || '获取结果失败');
      } finally {
        setIsLoading(false);
      }
    };

    fetchResult();
  }, [analysisId, navigate]);

  if (isLoading) {
    return (
      <div className="container mx-auto px-4 py-8 max-w-6xl">
        <div className="bg-white p-8 rounded-lg shadow text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">加载结果中...</p>
        </div>
      </div>
    );
  }

  if (error || !result) {
    return (
      <div className="container mx-auto px-4 py-8 max-w-6xl">
        <div className="bg-white p-8 rounded-lg shadow text-center">
          <div className="text-red-600 text-5xl mb-4">✕</div>
          <h2 className="text-2xl font-bold mb-4">加载失败</h2>
          <p className="text-gray-600 mb-6">{error || '未找到分析结果'}</p>
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

  const tabs = [
    { key: 'extraction' as const, label: '职业信息', icon: '📋' },
    { key: 'analysis' as const, label: '价值分析', icon: '💎' },
    { key: 'narrative' as const, label: '叙事策略', icon: '📖' },
    { key: 'resume' as const, label: '优化简历', icon: '✨' },
  ];

  return (
    <div className="container mx-auto px-4 py-8 max-w-6xl">
      {/* 头部 */}
      <div className="bg-white p-6 rounded-lg shadow mb-6">
        <div className="flex justify-between items-start">
          <div>
            <h1 className="text-3xl font-bold mb-2">职业价值分析报告</h1>
            <p className="text-gray-600">
              分析ID: {result.analysis_id} | 完成时间: {new Date(result.completed_at).toLocaleString('zh-CN')}
            </p>
          </div>
          <button
            onClick={() => navigate('/dashboard')}
            className="px-4 py-2 border border-gray-300 rounded hover:bg-gray-50"
          >
            返回首页
          </button>
        </div>

        {/* 统计信息 */}
        {result.stats && (
          <div className="mt-6 grid grid-cols-4 gap-4">
            <div className="p-4 bg-blue-50 rounded-lg">
              <div className="text-sm text-gray-600">处理时间</div>
              <div className="text-2xl font-bold text-blue-600">
                {Math.round(result.stats.total_time)}秒
              </div>
            </div>
            <div className="p-4 bg-green-50 rounded-lg">
              <div className="text-sm text-gray-600">总成本</div>
              <div className="text-2xl font-bold text-green-600">
                ${result.stats.total_cost.toFixed(3)}
              </div>
            </div>
            <div className="p-4 bg-purple-50 rounded-lg">
              <div className="text-sm text-gray-600">Token使用</div>
              <div className="text-2xl font-bold text-purple-600">
                {result.stats.total_tokens.toLocaleString()}
              </div>
            </div>
            <div className="p-4 bg-orange-50 rounded-lg">
              <div className="text-sm text-gray-600">API调用</div>
              <div className="text-2xl font-bold text-orange-600">
                {result.stats.total_api_calls}次
              </div>
            </div>
          </div>
        )}
      </div>

      {/* 标签页 */}
      <div className="bg-white rounded-lg shadow">
        <div className="border-b border-gray-200">
          <div className="flex">
            {tabs.map((tab) => (
              <button
                key={tab.key}
                onClick={() => setActiveTab(tab.key)}
                className={`flex-1 px-6 py-4 text-center font-medium transition ${
                  activeTab === tab.key
                    ? 'border-b-2 border-blue-600 text-blue-600'
                    : 'text-gray-600 hover:text-gray-900'
                }`}
              >
                <span className="mr-2">{tab.icon}</span>
                {tab.label}
              </button>
            ))}
          </div>
        </div>

        <div className="p-6">
          {/* 职业信息提取 */}
          {activeTab === 'extraction' && result.extraction && (
            <div className="space-y-6">
              <Section title="基本信息">
                <InfoGrid>
                  <InfoItem label="目标岗位" value={result.extraction.target_role} />
                  <InfoItem label="目标行业" value={result.extraction.target_industry || '未指定'} />
                </InfoGrid>
              </Section>

              <Section title="工作经历">
                {result.extraction.work_experiences?.map((exp, idx) => (
                  <div key={idx} className="mb-4 p-4 bg-gray-50 rounded">
                    <h4 className="font-medium">{exp.title} @ {exp.company}</h4>
                    <p className="text-sm text-gray-600">{exp.duration}</p>
                    <ul className="mt-2 space-y-1">
                      {exp.responsibilities?.map((resp, i) => (
                        <li key={i} className="text-sm">• {resp}</li>
                      ))}
                    </ul>
                  </div>
                ))}
              </Section>

              <Section title="核心技能">
                <div className="flex flex-wrap gap-2">
                  {result.extraction.skills?.map((skill, idx) => (
                    <span key={idx} className="px-3 py-1 bg-blue-100 text-blue-700 rounded-full text-sm">
                      {skill}
                    </span>
                  ))}
                </div>
              </Section>

              <Section title="主要成就">
                <ul className="space-y-2">
                  {result.extraction.achievements?.map((achievement, idx) => (
                    <li key={idx} className="flex items-start">
                      <span className="text-green-600 mr-2">✓</span>
                      <span>{achievement}</span>
                    </li>
                  ))}
                </ul>
              </Section>
            </div>
          )}

          {/* 价值分析 */}
          {activeTab === 'analysis' && result.analysis && (
            <div className="space-y-6">
              <Section title="价值主张">
                <p className="text-lg leading-relaxed">{result.analysis.value_proposition}</p>
              </Section>

              <Section title="可迁移技能">
                <div className="grid grid-cols-2 gap-4">
                  {result.analysis.transferable_skills?.map((skill, idx) => (
                    <div key={idx} className="p-4 bg-blue-50 rounded">
                      <h4 className="font-medium text-blue-900">{skill.skill}</h4>
                      <p className="text-sm text-gray-600 mt-1">{skill.evidence}</p>
                    </div>
                  ))}
                </div>
              </Section>

              <Section title="量化成果">
                <div className="space-y-3">
                  {result.analysis.quantified_achievements?.map((achievement, idx) => (
                    <div key={idx} className="p-4 bg-green-50 rounded">
                      <div className="flex justify-between items-start">
                        <div className="flex-1">
                          <h4 className="font-medium text-green-900">{achievement.achievement}</h4>
                          <p className="text-sm text-gray-600 mt-1">{achievement.context}</p>
                        </div>
                        <div className="text-2xl font-bold text-green-600 ml-4">
                          {achievement.metric}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </Section>

              <Section title="能力图谱">
                <div className="grid grid-cols-3 gap-4">
                  {result.analysis.capability_map?.map((cap, idx) => (
                    <div key={idx} className="p-4 bg-purple-50 rounded text-center">
                      <div className="text-3xl mb-2">{cap.icon || '⭐'}</div>
                      <h4 className="font-medium">{cap.category}</h4>
                      <div className="mt-2 space-y-1">
                        {cap.skills?.map((skill, i) => (
                          <div key={i} className="text-sm text-gray-600">{skill}</div>
                        ))}
                      </div>
                    </div>
                  ))}
                </div>
              </Section>
            </div>
          )}

          {/* 叙事策略 */}
          {activeTab === 'narrative' && result.narrative && (
            <div className="space-y-6">
              <Section title="职业故事">
                <p className="text-lg leading-relaxed whitespace-pre-wrap">{result.narrative.career_story}</p>
              </Section>

              <Section title="故事弧线">
                <div className="space-y-4">
                  {result.narrative.story_arc?.map((arc, idx) => (
                    <div key={idx} className="p-4 bg-gray-50 rounded">
                      <h4 className="font-medium text-lg mb-2">{arc.phase}</h4>
                      <p className="text-gray-700">{arc.narrative}</p>
                    </div>
                  ))}
                </div>
              </Section>

              <Section title="定位陈述">
                <div className="p-6 bg-blue-50 rounded-lg border-l-4 border-blue-600">
                  <p className="text-lg font-medium">{result.narrative.positioning_statement}</p>
                </div>
              </Section>

              <Section title="差异化优势">
                <ul className="space-y-3">
                  {result.narrative.differentiation_points?.map((point, idx) => (
                    <li key={idx} className="flex items-start p-3 bg-yellow-50 rounded">
                      <span className="text-yellow-600 mr-3 text-xl">★</span>
                      <span className="flex-1">{point}</span>
                    </li>
                  ))}
                </ul>
              </Section>
            </div>
          )}

          {/* 优化简历 */}
          {activeTab === 'resume' && result.resume && (
            <div className="space-y-6">
              <Section title="简历摘要">
                <p className="text-lg leading-relaxed">{result.resume.summary}</p>
              </Section>

              <Section title="工作经历">
                {result.resume.work_experience?.map((exp, idx) => (
                  <div key={idx} className="mb-6 p-4 bg-gray-50 rounded">
                    <div className="flex justify-between items-start mb-2">
                      <div>
                        <h4 className="font-bold text-lg">{exp.title}</h4>
                        <p className="text-gray-600">{exp.company}</p>
                      </div>
                      <span className="text-sm text-gray-500">{exp.duration}</span>
                    </div>
                    <ul className="mt-3 space-y-2">
                      {exp.highlights?.map((highlight, i) => (
                        <li key={i} className="flex items-start">
                          <span className="mr-2">•</span>
                          <span>{highlight}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                ))}
              </Section>

              <Section title="核心技能">
                <div className="grid grid-cols-3 gap-4">
                  {result.resume.skills?.map((skillGroup, idx) => (
                    <div key={idx} className="p-4 bg-blue-50 rounded">
                      <h4 className="font-medium mb-2">{skillGroup.category}</h4>
                      <div className="flex flex-wrap gap-2">
                        {skillGroup.items?.map((item, i) => (
                          <span key={i} className="text-sm text-gray-700">{item}</span>
                        ))}
                      </div>
                    </div>
                  ))}
                </div>
              </Section>

              <Section title="ATS关键词">
                <div className="flex flex-wrap gap-2">
                  {result.resume.ats_keywords?.map((keyword, idx) => (
                    <span key={idx} className="px-3 py-1 bg-green-100 text-green-700 rounded text-sm">
                      {keyword}
                    </span>
                  ))}
                </div>
              </Section>
            </div>
          )}
        </div>
      </div>

      {/* 操作按钮 */}
      <div className="mt-6 flex justify-center gap-4">
        <button
          onClick={() => window.print()}
          className="px-6 py-3 bg-gray-600 text-white rounded hover:bg-gray-700"
        >
          打印报告
        </button>
        <button
          onClick={() => navigate('/analysis/new')}
          className="px-6 py-3 bg-blue-600 text-white rounded hover:bg-blue-700"
        >
          开始新分析
        </button>
      </div>
    </div>
  );
}

// 辅助组件
function Section({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <div>
      <h3 className="text-xl font-bold mb-4 pb-2 border-b border-gray-200">{title}</h3>
      <div>{children}</div>
    </div>
  );
}

function InfoGrid({ children }: { children: React.ReactNode }) {
  return <div className="grid grid-cols-2 gap-4">{children}</div>;
}

function InfoItem({ label, value }: { label: string; value: string }) {
  return (
    <div className="p-3 bg-gray-50 rounded">
      <div className="text-sm text-gray-600">{label}</div>
      <div className="font-medium mt-1">{value}</div>
    </div>
  );
}
