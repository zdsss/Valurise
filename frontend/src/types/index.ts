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
export interface WorkExperience {
  company: string;
  position: string;
  start_date: string;
  end_date: string;
  responsibilities: string[];
  achievements: string[];
}

export interface Education {
  institution: string;
  degree: string;
  field: string;
  graduation_date: string;
}

export interface TargetRole {
  title: string;
  industry: string;
  key_requirements: string[];
}

export interface AnalysisInput {
  raw_text?: string;
  work_experiences: WorkExperience[];
  education: Education[];
  skills: string[];
}

export interface AnalysisOptions {
  num_resume_versions: number;
  include_linkedin: boolean;
}

export interface AnalysisCreateRequest {
  input_data: AnalysisInput;
  target_role: TargetRole;
  options?: AnalysisOptions;
}

export interface Analysis {
  id: string;
  status: 'pending' | 'processing' | 'completed' | 'failed';
  created_at: string;
  started_at?: string;
  completed_at?: string;
}

export interface AnalysisProgress {
  current_step: number;
  total_steps: number;
  current_agent: string;
  message: string;
  progress_percentage: number;
}

export interface AnalysisStatus extends Analysis {
  progress?: AnalysisProgress;
  estimated_completion?: string;
}

export interface AnalysisResult {
  extracted_info: Record<string, any>;
  value_analysis: Record<string, any>;
  narrative_strategy: Record<string, any>;
  resume_versions: Record<string, any>[];
}

export interface AnalysisMetadata {
  cost: number;
  processing_time_seconds: number;
  completed_at: string;
}

export interface AnalysisResultResponse extends Analysis {
  result: AnalysisResult;
  metadata: AnalysisMetadata;
}

export interface AnalysisHistoryItem {
  id: string;
  status: string;
  target_role: string;
  created_at: string;
  completed_at?: string;
  cost?: number;
}

// 支付相关类型
export interface CreateCheckoutRequest {
  product_tier: 'basic' | 'pro' | 'premium';
  success_url: string;
  cancel_url: string;
}

export interface CreateCheckoutResponse {
  checkout_session_id: string;
  checkout_url: string;
  order_id: string;
}

export interface PaymentVerifyResponse {
  order_id: string;
  status: string;
  product_tier: string;
  amount_cents: number;
  paid_at?: string;
  analysis_id?: string;
}

// API错误类型
export interface APIError {
  error: {
    code: string;
    message: string;
    details?: any;
  };
}
