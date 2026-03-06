import { Link } from 'react-router-dom';

export default function HomePage() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white">
      {/* Hero Section */}
      <div className="container mx-auto px-4 py-16">
        <div className="max-w-4xl mx-auto text-center">
          <h1 className="text-5xl md:text-6xl font-bold mb-6 bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
            发现你的职业价值
          </h1>
          <p className="text-xl md:text-2xl text-gray-600 mb-8">
            AI驱动的职业价值分析平台，帮助你重新认识自己的职业优势
          </p>
          <div className="flex gap-4 justify-center flex-wrap">
            <Link
              to="/register"
              className="px-8 py-4 bg-blue-600 text-white rounded-lg text-lg font-medium hover:bg-blue-700 transition shadow-lg"
            >
              免费开始
            </Link>
            <Link
              to="/pricing"
              className="px-8 py-4 border-2 border-gray-300 rounded-lg text-lg font-medium hover:border-blue-500 hover:bg-blue-50 transition"
            >
              查看定价
            </Link>
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div className="container mx-auto px-4 py-16">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-3xl font-bold text-center mb-12">核心功能</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="p-8 bg-white border-2 border-gray-200 rounded-lg hover:border-blue-500 hover:shadow-lg transition">
              <div className="text-5xl mb-4">💎</div>
              <h3 className="text-2xl font-semibold mb-3">深度价值分析</h3>
              <p className="text-gray-600 leading-relaxed">
                AI深度分析你的工作经历，挖掘隐藏的职业价值，识别可迁移技能，量化关键成就
              </p>
            </div>
            <div className="p-8 bg-white border-2 border-gray-200 rounded-lg hover:border-blue-500 hover:shadow-lg transition">
              <div className="text-5xl mb-4">📖</div>
              <h3 className="text-2xl font-semibold mb-3">职业叙事策略</h3>
              <p className="text-gray-600 leading-relaxed">
                构建有说服力的职业故事，设计完整的故事弧线，展现你的独特优势和差异化价值
              </p>
            </div>
            <div className="p-8 bg-white border-2 border-gray-200 rounded-lg hover:border-blue-500 hover:shadow-lg transition">
              <div className="text-5xl mb-4">✨</div>
              <h3 className="text-2xl font-semibold mb-3">简历优化</h3>
              <p className="text-gray-600 leading-relaxed">
                生成针对目标岗位的优化简历，ATS关键词优化，量化成果展示，提高通过率
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* How It Works */}
      <div className="bg-gray-50 py-16">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto">
            <h2 className="text-3xl font-bold text-center mb-12">如何使用</h2>
            <div className="space-y-8">
              <div className="flex items-start gap-6">
                <div className="flex-shrink-0 w-12 h-12 bg-blue-600 text-white rounded-full flex items-center justify-center text-xl font-bold">
                  1
                </div>
                <div>
                  <h3 className="text-xl font-semibold mb-2">输入职业信息</h3>
                  <p className="text-gray-600">
                    详细描述你的工作经历、项目经验、技能特长和主要成就
                  </p>
                </div>
              </div>
              <div className="flex items-start gap-6">
                <div className="flex-shrink-0 w-12 h-12 bg-blue-600 text-white rounded-full flex items-center justify-center text-xl font-bold">
                  2
                </div>
                <div>
                  <h3 className="text-xl font-semibold mb-2">AI深度分析</h3>
                  <p className="text-gray-600">
                    4个专业化AI Agent协同工作，从信息提取到简历优化，全流程自动化处理
                  </p>
                </div>
              </div>
              <div className="flex items-start gap-6">
                <div className="flex-shrink-0 w-12 h-12 bg-blue-600 text-white rounded-full flex items-center justify-center text-xl font-bold">
                  3
                </div>
                <div>
                  <h3 className="text-xl font-semibold mb-2">获取完整报告</h3>
                  <p className="text-gray-600">
                    获得详细的职业价值分析报告、叙事策略和优化后的简历
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Stats Section */}
      <div className="container mx-auto px-4 py-16">
        <div className="max-w-4xl mx-auto">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 text-center">
            <div>
              <div className="text-4xl font-bold text-blue-600 mb-2">2-4分钟</div>
              <p className="text-gray-600">平均处理时间</p>
            </div>
            <div>
              <div className="text-4xl font-bold text-blue-600 mb-2">4.6/5</div>
              <p className="text-gray-600">用户满意度</p>
            </div>
            <div>
              <div className="text-4xl font-bold text-blue-600 mb-2">$0.17</div>
              <p className="text-gray-600">平均分析成本</p>
            </div>
          </div>
        </div>
      </div>

      {/* CTA Section */}
      <div className="bg-blue-600 text-white py-16">
        <div className="container mx-auto px-4 text-center">
          <h2 className="text-3xl md:text-4xl font-bold mb-4">
            准备好发现你的职业价值了吗？
          </h2>
          <p className="text-xl mb-8 text-blue-100">
            立即开始，只需几分钟
          </p>
          <Link
            to="/register"
            className="inline-block px-8 py-4 bg-white text-blue-600 rounded-lg text-lg font-medium hover:bg-gray-100 transition shadow-lg"
          >
            免费注册
          </Link>
        </div>
      </div>
    </div>
  );
}
