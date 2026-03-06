import { Outlet, Link } from 'react-router-dom';

export default function AuthLayout() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <Link to="/" className="text-3xl font-bold text-blue-600">
            Valurise
          </Link>
          <p className="text-gray-600 mt-2">AI驱动的职业价值发现平台</p>
        </div>
        <Outlet />
      </div>
    </div>
  );
}
