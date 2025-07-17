declare module 'axios' {
  export interface AxiosRequestConfig {
    baseURL?: string;
    timeout?: number;
    headers?: Record<string, string>;
    params?: any;
    data?: any;
    method?: string;
    url?: string;
    responseType?: string;
  }

  export interface AxiosResponse<T = any> {
    data: T;
    status: number;
    statusText: string;
    headers: Record<string, string>;
    config: AxiosRequestConfig;
  }

  export interface AxiosError<T = any> extends Error {
    config: AxiosRequestConfig;
    code?: string;
    request?: any;
    response?: AxiosResponse<T>;
    isAxiosError: boolean;
  }

  export interface AxiosInstance {
    (config: AxiosRequestConfig): Promise<AxiosResponse>;
    (url: string, config?: AxiosRequestConfig): Promise<AxiosResponse>;
    defaults: AxiosRequestConfig;
    get<T = any>(url: string, config?: AxiosRequestConfig): Promise<AxiosResponse<T>>;
    post<T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<AxiosResponse<T>>;
    put<T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<AxiosResponse<T>>;
    delete<T = any>(url: string, config?: AxiosRequestConfig): Promise<AxiosResponse<T>>;
  }

  export function create(config?: AxiosRequestConfig): AxiosInstance;

  const axios: AxiosInstance & {
    create: typeof create;
    CancelToken: any;
    isCancel: (value: any) => boolean;
    all: <T>(values: Array<T | Promise<T>>) => Promise<T[]>;
    spread: <T, R>(callback: (...args: T[]) => R) => (array: T[]) => R;
  };

  export default axios;
} 