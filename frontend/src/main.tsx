import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.tsx'

// 验证必需的环境变量
const requiredEnvVars = {
  VITE_API_URL: import.meta.env.VITE_API_URL,
};

const missingEnvVars = Object.entries(requiredEnvVars)
  .filter(([, value]) => !value)
  .map(([key]) => key);

if (missingEnvVars.length > 0) {
  const errorMessage = `
    ❌ 缺少必需的环境变量:
    ${missingEnvVars.map(key => `  - ${key}`).join('\n')}

    请创建 .env 文件并配置以下变量:
    ${missingEnvVars.map(key => `  ${key}=your_value_here`).join('\n')}

    参考 .env.example 文件获取更多信息。
  `;

  console.error(errorMessage);

  // 显示友好的错误页面
  document.getElementById('root')!.innerHTML = `
    <div style="
      display: flex;
      align-items: center;
      justify-content: center;
      min-height: 100vh;
      background: #f3f4f6;
      font-family: system-ui, -apple-system, sans-serif;
      padding: 20px;
    ">
      <div style="
        max-width: 600px;
        background: white;
        padding: 40px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
      ">
        <div style="font-size: 48px; margin-bottom: 20px;">⚠️</div>
        <h1 style="font-size: 24px; font-weight: bold; margin-bottom: 16px; color: #1f2937;">
          配置错误
        </h1>
        <p style="color: #6b7280; margin-bottom: 24px;">
          应用缺少必需的环境变量配置。
        </p>
        <div style="
          background: #fef2f2;
          border: 1px solid #fecaca;
          border-radius: 8px;
          padding: 16px;
          margin-bottom: 24px;
        ">
          <p style="font-weight: 600; color: #991b1b; margin-bottom: 8px;">
            缺少的环境变量:
          </p>
          <ul style="color: #991b1b; margin-left: 20px;">
            ${missingEnvVars.map(key => `<li><code>${key}</code></li>`).join('')}
          </ul>
        </div>
        <div style="
          background: #eff6ff;
          border: 1px solid #bfdbfe;
          border-radius: 8px;
          padding: 16px;
        ">
          <p style="font-weight: 600; color: #1e40af; margin-bottom: 8px;">
            解决方法:
          </p>
          <ol style="color: #1e40af; margin-left: 20px;">
            <li>在项目根目录创建 <code>.env</code> 文件</li>
            <li>参考 <code>.env.example</code> 文件配置环境变量</li>
            <li>重新启动开发服务器</li>
          </ol>
        </div>
      </div>
    </div>
  `;

  throw new Error('Missing required environment variables');
}

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
