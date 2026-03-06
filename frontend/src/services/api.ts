import axios, { AxiosInstance, AxiosError } from 'axios';
import type {
  LoginRequest,
  RegisterRequest,
  AuthResponse,
  UserDetail,
  AnalysisCreateRequest,
  AnalysisStatus,
  AnalysisResultResponse,
  AnalysisHistoryItem,
  CreateCheckoutRequest,
  CreateCheckoutResponse,
  PaymentVerifyResponse,
  APIError,
} from '../types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

class APIClient {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // 请求拦截器：添加认证token
    this.client.interceptors.request.use(
      (config) => {
        const token = localStorage.getItem('access_token');
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => Promise.reject(error)
    );

    // 响应拦截器：处理错误
    this.client.interceptors.response.use(
      (response) => response,
      async (error: AxiosError<APIError>) => {
        if (error.response?.status === 401) {
          // Token过期，清除本地存储
          localStorage.removeItem('access_token');
          localStorage.removeItem('refresh_token');
          window.location.href = '/login';
        }
        return Promise.reject(error);
      }
    );
  }

  // 认证相关
  async register(data: RegisterRequest): Promise<AuthResponse> {
    const response = await this.client.post<AuthResponse>('/auth/register', data);
    return response.data;
  }

  async login(data: LoginRequest): Promise<AuthResponse> {
    const response = await this.client.post<AuthResponse>('/auth/login', data);
    return response.data;
  }

  async refreshToken(refreshToken: string): Promise<{ access_token: string; token_type: string }> {
    const response = await this.client.post('/auth/refresh', { refresh_token: refreshToken });
    return response.data;
  }

  // 用户相关
  async getCurrentUser(): Promise<UserDetail> {
    const response = await this.client.get<UserDetail>('/users/me');
    return response.data;
  }

  async updateUser(data: { full_name?: string }): Promise<UserDetail> {
    const response = await this.client.patch<UserDetail>('/users/me', data);
    return response.data;
  }

  // 分析相关
  async createAnalysis(data: AnalysisCreateRequest): Promise<{ analysis_id: string; status: string; estimated_time_seconds: number; created_at: string }> {
    const response = await this.client.post('/analyses', data);
    return response.data;
  }

  async getAnalysisStatus(analysisId: string): Promise<AnalysisStatus> {
    const response = await this.client.get<AnalysisStatus>(`/analyses/${analysisId}`);
    return response.data;
  }

  async getAnalysisResult(analysisId: string): Promise<AnalysisResultResponse> {
    const response = await this.client.get<AnalysisResultResponse>(`/analyses/${analysisId}/result`);
    return response.data;
  }

  async getAnalysisHistory(page: number = 1, limit: number = 10, status?: string): Promise<{ analyses: AnalysisHistoryItem[]; pagination: any }> {
    const params: any = { page, limit };
    if (status) params.status = status;
    const response = await this.client.get('/analyses', { params });
    return response.data;
  }

  // 支付相关
  async createCheckout(data: CreateCheckoutRequest): Promise<CreateCheckoutResponse> {
    const response = await this.client.post<CreateCheckoutResponse>('/payment/create-checkout', data);
    return response.data;
  }

  async verifyPayment(sessionId: string): Promise<PaymentVerifyResponse> {
    const response = await this.client.get<PaymentVerifyResponse>(`/payment/verify/${sessionId}`);
    return response.data;
  }
}

export const apiClient = new APIClient();
