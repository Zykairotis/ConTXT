import * as api from './api';
import * as capture from './contentCapture';
import * as storage from './storage';
import { CapturedContent, ApiResponse } from '../types';

/**
 * Ingestion result
 */
export interface IngestionResult {
  success: boolean;
  jobId?: string;
  contentType: string;
  timestamp: number;
  error?: string;
}

/**
 * Ingest the current URL
 * @returns The ingestion result
 */
export async function ingestCurrentUrl(): Promise<IngestionResult> {
  try {
    // Capture URL content
    const content = await capture.captureUrl();
    
    // Save to storage first
    await storage.saveCapturedContent(content);
    
    // Send to backend
    const response = await api.sendContent(content);
    
    if (!response.success) {
      return {
        success: false,
        contentType: content.type,
        timestamp: content.metadata.timestamp,
        error: response.error,
      };
    }
    
    return {
      success: true,
      jobId: response.data?.jobId,
      contentType: content.type,
      timestamp: content.metadata.timestamp,
    };
  } catch (error: any) {
    console.error('Error ingesting URL:', error);
    return {
      success: false,
      contentType: 'url',
      timestamp: Date.now(),
      error: error.message || 'Failed to ingest URL',
    };
  }
}

/**
 * Ingest selected text from the current page
 * @returns The ingestion result
 */
export async function ingestSelectedText(): Promise<IngestionResult> {
  try {
    // Capture selected text
    const content = await capture.captureSelectedText();
    
    // Save to storage first
    await storage.saveCapturedContent(content);
    
    // Send to backend
    const response = await api.sendContent(content);
    
    if (!response.success) {
      return {
        success: false,
        contentType: content.type,
        timestamp: content.metadata.timestamp,
        error: response.error,
      };
    }
    
    return {
      success: true,
      jobId: response.data?.jobId,
      contentType: content.type,
      timestamp: content.metadata.timestamp,
    };
  } catch (error: any) {
    console.error('Error ingesting selected text:', error);
    return {
      success: false,
      contentType: 'text',
      timestamp: Date.now(),
      error: error.message || 'Failed to ingest selected text',
    };
  }
}

/**
 * Ingest a screenshot of the current page
 * @returns The ingestion result
 */
export async function ingestScreenshot(): Promise<IngestionResult> {
  try {
    // Capture screenshot
    const content = await capture.captureVisibleContent();
    
    // Save to storage first
    await storage.saveCapturedContent(content);
    
    // Send to backend
    const response = await api.sendContent(content);
    
    if (!response.success) {
      return {
        success: false,
        contentType: content.type,
        timestamp: content.metadata.timestamp,
        error: response.error,
      };
    }
    
    return {
      success: true,
      jobId: response.data?.jobId,
      contentType: content.type,
      timestamp: content.metadata.timestamp,
    };
  } catch (error: any) {
    console.error('Error ingesting screenshot:', error);
    return {
      success: false,
      contentType: 'image',
      timestamp: Date.now(),
      error: error.message || 'Failed to ingest screenshot',
    };
  }
}

/**
 * Ingest HTML content from the current page
 * @returns The ingestion result
 */
export async function ingestPageContent(): Promise<IngestionResult> {
  try {
    // Capture HTML
    const content = await capture.capturePageContent();
    
    // Save to storage first
    await storage.saveCapturedContent(content);
    
    // Send to backend
    const response = await api.sendContent(content);
    
    if (!response.success) {
      return {
        success: false,
        contentType: content.type,
        timestamp: content.metadata.timestamp,
        error: response.error,
      };
    }
    
    return {
      success: true,
      jobId: response.data?.jobId,
      contentType: content.type,
      timestamp: content.metadata.timestamp,
    };
  } catch (error: any) {
    console.error('Error ingesting HTML:', error);
    return {
      success: false,
      contentType: 'html',
      timestamp: Date.now(),
      error: error.message || 'Failed to ingest HTML',
    };
  }
}

/**
 * Ingest chat content from the current page
 * @returns The ingestion result
 */
export async function ingestChatContent(): Promise<IngestionResult> {
  try {
    // Capture chat
    const content = await capture.captureChatContent();
    
    // Save to storage first
    await storage.saveCapturedContent(content);
    
    // Send to backend
    const response = await api.sendContent(content);
    
    if (!response.success) {
      return {
        success: false,
        contentType: content.type,
        timestamp: content.metadata.timestamp,
        error: response.error,
      };
    }
    
    return {
      success: true,
      jobId: response.data?.jobId,
      contentType: content.type,
      timestamp: content.metadata.timestamp,
    };
  } catch (error: any) {
    console.error('Error ingesting chat content:', error);
    return {
      success: false,
      contentType: 'text',
      timestamp: Date.now(),
      error: error.message || 'Failed to ingest chat content',
    };
  }
}

/**
 * Check the status of an ingestion job
 * @param jobId The ID of the job to check
 * @returns The status information
 */
export async function checkStatus(jobId: string): Promise<ApiResponse<any>> {
  return api.checkStatus(jobId);
} 