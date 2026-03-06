import { Link } from 'react-router-dom';

export default function HomePage() {
  return (
    <div className="container mx-auto px-4 py-16">
      <div className="max-w-4xl mx-auto text-center">
        <h1 className="text-5xl font-bold mb-6">
          发现你的职业价值
        </h1>
        <p className="text-xl text-muted-foreground mb-8">
          AI驱动的职业价值分析平台，帮助你重新认识自己的职业优势
        </p>
        <div className="flex gap-4 justify-center">
          <Link
            to="/register"
            className="px-8 py-3 bg-primary text-primary-foreground rounded-lg text-lg font-medium hover:bg-primary/90"
          >
            开始使用
          </Link>
          <Link
            to="/pricing"
            className="px-8 py-3 border border-input rounded-lg text-lg font-medium hover:bg-accent"
          >
            查看定价
          </Link>
        </div>

        <div className="mt-16 grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="p-6 border rounded-lg">
            <h3 className="text-xl font-semibold mb-2">深度价值分析</h3>
            <p className="text-muted-foreground">
              AI分析你的工作经历，挖掘隐藏的职业价值
            </p>
          </div>
          <div className="p-6 border rounded-lg">
            <h3 className="text-xl font-semibold mb-2">职业叙事策略</h3>
            <p className="text-muted-foreground">
              构建有说服力的职业故事，展现你的独特优势
            </p>
          </div>
          <div className="p-6 border rounded-lg">
            <h3 className="text-xl font-semibold mb-2">简历优化</h3>
            <p className="text-muted-foreground">
              生成针对目标岗位的优化简历，提高通过率
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
