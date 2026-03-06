// 用户相关类型
export interface User {
  id: string;
  email: string;
  full_name: string | null;
  subscription_tier: string;
  credits_remaining: number;
  created_at: string;
  is_active: boolean;
  is_verified: boolean;
}

export interface UserStats {
  total_analyses: number;
  completed_analyses: number;
  total_spent_cents: number;
}

export interface UserDetail extends User {
  stats: UserStats;
}

// 认证相关类型
export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  email: string;
  password: string;
  full_name?: string;
}

export interface AuthResponse {
  user: User;
  access_token: string;
  refresh_token?: string;
  token_type: string;
}

// 分析相关类型
export interface AnalysisCreateRequest {
  raw_input: string;
  target_role: string;
  target_industry?: string;
}

export interface AnalysisStatus {
  analysis_id: string;
  status: 'pending' | 'processing' | 'completed' | 'failed';
  current_step: string;
  created_at: string;
  started_at?: string;
  completed_at?: string;
  error_message?: string;
  stats?: {
    elapsed_time: number;
    estimated_remaining_time: number;
  };
}

export interface AnalysisResultResponse {
  analysis_id: string;
  status: string;
  created_at: string;
  completed_at: string;
  extraction?: any;
  analysis?: any;
  narrative?: any;
  resume?: any;
  stats?: {
    total_time: number;
    total_cost: number;
    total_tokens: number;
    total_api_calls: number;
  };
}

export interface AnalysisHistoryItem {
  id: string;
  status: string;
  target_role: string;
  target_industry?: string;
  created_at: string;
  completed_at?: string;
  cost?: number;
}

// 支付相关类型
export interface CreateCheckoutRequest {
  price_id: string;
  success_url: string;
  cancel_url: string;
}

export interface CreateCheckoutResponse {
  checkout_url: string;
  session_id: string;
}

export interface PaymentVerifyResponse {
  order_id: string;
  status: string;
  amount: number;
  paid_at?: string;
}

// API错误类型
export interface APIError {
  error: {
    code: string;
    message: string;
    details?: any;
  };
}
