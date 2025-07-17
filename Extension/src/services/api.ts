import axios, { AxiosInstance, AxiosRequestConfig } from 'axios';
import { CapturedContent, ApiResponse } from '../types';
import { API_BASE_URL, API_ENDPOINTS } from '../constants';
import * as storage from './storage';

/**
 * Create an API client instance
 */
const createApiClient = async (): Promise<AxiosInstance> => {
  // Get the server URL from storage or use the default
  const serverUrl = await storage.getServerUrl() || API_BASE_URL;
  const apiKey = await storage.getApiKey();
  
  const config: AxiosRequestConfig = {
    baseURL: serverUrl,
    timeout: 30000, // 30 seconds
    headers: {
      'Content-Type': 'application/json',
    },
  };
  
  // Add API key if available
  if (apiKey) {
    config.headers = {
      ...config.headers,
      'Authorization': `Bearer ${apiKey}`,
    };
  }
  
  return axios.create(config);
};

/**
 * Send captured content to the API
 * @param content The captured content to send
 * @returns API response
 */
export async function sendContent(content: CapturedContent): Promise<ApiResponse<any>> {
  try {
    const client = await createApiClient();
    const response = await client.post(API_ENDPOINTS.INGEST, content);
    return {
      success: true,
      data: response.data,
    };
  } catch (error: any) {
    console.error('Error sending content to API:', error);
    return {
      success: false,
      error: error.message || 'Failed to send content to API',
    };
  }
}

/**
 * Check the status of a processing job
 * @param jobId The ID of the job to check
 * @returns API response with status information
 */
export async function checkStatus(jobId: string): Promise<ApiResponse<any>> {
  try {
    const client = await createApiClient();
    const response = await client.get(`${API_ENDPOINTS.STATUS}/${jobId}`);
    return {
      success: true,
      data: response.data,
    };
  } catch (error: any) {
    console.error('Error checking job status:', error);
    return {
      success: false,
      error: error.message || 'Failed to check job status',
    };
  }
}

/**
 * Verify the API connection
 * @returns Whether the API is reachable
 */
export async function verifyConnection(): Promise<boolean> {
  try {
    const client = await createApiClient();
    await client.get('/health');
    return true;
  } catch (error) {
    console.error('API connection failed:', error);
    return false;
  }
} 