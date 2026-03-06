import axios, { type AxiosInstance, AxiosError } from 'axios';
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

// 错误消息映射
const ERROR_MESSAGES: Record<string, string> = {
  // 认证错误
  'INVALID_CREDENTIALS': '邮箱或密码错误，请重试',
  'USER_EXISTS': '该邮箱已被注册，请直接登录',
  'USER_NOT_FOUND': '用户不存在',
  'INVALID_TOKEN': '登录已过期，请重新登录',
  'TOKEN_EXPIRED': '登录已过期，请重新登录',

  // 分析错误
  'ANALYSIS_NOT_FOUND': '分析记录不存在',
  'INSUFFICIENT_CREDITS': '积分不足，请先购买',
  'ANALYSIS_FAILED': '分析失败，请重试',
  'INVALID_INPUT': '输入内容不符合要求，请检查后重试',

  // 支付错误
  'PAYMENT_FAILED': '支付失败，请重试',
  'INVALID_PAYMENT': '支付信息无效',
  'ORDER_NOT_FOUND': '订单不存在',

  // 通用错误
  'NETWORK_ERROR': '网络连接失败，请检查网络后重试',
  'SERVER_ERROR': '服务器错误，请稍后重试',
  'VALIDATION_ERROR': '输入信息有误，请检查后重试',
  'RATE_LIMIT': '请求过于频繁，请稍后再试',
  'UNKNOWN_ERROR': '发生未知错误，请联系客服',
};

// 获取友好的错误消息
function getFriendlyErrorMessage(error: AxiosError<APIError>): string {
  // 网络错误
  if (!error.response) {
    return ERROR_MESSAGES['NETWORK_ERROR'];
  }

  // 从响应中获取错误代码
  const errorCode = error.response.data?.error?.code;
  if (errorCode && ERROR_MESSAGES[errorCode]) {
    return ERROR_MESSAGES[errorCode];
  }

  // 从响应中获取错误消息
  const errorMessage = error.response.data?.error?.message;
  if (errorMessage) {
    return errorMessage;
  }

  // 根据HTTP状态码返回默认消息
  switch (error.response.status) {
    case 400:
      return ERROR_MESSAGES['VALIDATION_ERROR'];
    case 401:
      return ERROR_MESSAGES['INVALID_TOKEN'];
    case 403:
      return '没有权限执行此操作';
    case 404:
      return '请求的资源不存在';
    case 429:
      return ERROR_MESSAGES['RATE_LIMIT'];
    case 500:
    case 502:
    case 503:
      return ERROR_MESSAGES['SERVER_ERROR'];
    default:
      return ERROR_MESSAGES['UNKNOWN_ERROR'];
  }
}

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
        // 401错误：Token过期，跳转登录
        if (error.response?.status === 401) {
          localStorage.removeItem('access_token');
          localStorage.removeItem('refresh_token');
          window.location.href = '/login';
        }

        // 增强错误对象，添加友好的错误消息
        const enhancedError = error as AxiosError<APIError> & {
          friendlyMessage?: string;
        };
        enhancedError.friendlyMessage = getFriendlyErrorMessage(error);

        return Promise.reject(enhancedError);
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

// 导出错误消息获取函数，供组件使用
export function getErrorMessage(error: any): string {
  if (error?.friendlyMessage) {
    return error.friendlyMessage;
  }
  if (error?.response?.data?.error?.message) {
    return error.response.data.error.message;
  }
  if (error?.message) {
    return error.message;
  }
  return ERROR_MESSAGES['UNKNOWN_ERROR'];
}
