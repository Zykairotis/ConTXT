// Content types
export interface CapturedContent {
  type: 'text' | 'html' | 'image' | 'pdf' | 'url';
  content: string;
  metadata: {
    url: string;
    title: string;
    timestamp: number;
    source: string;
  };
}

// API types
export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
}

// Storage types
export interface StorageData {
  apiKey?: string;
  serverUrl?: string;
  settings?: UserSettings;
  capturedContent?: CapturedContent[];
}

export interface UserSettings {
  captureFormat: 'text' | 'html' | 'image';
  autoCapture: boolean;
  notificationsEnabled: boolean;
}

// Message types for communication between background, content scripts, and popup
export interface Message {
  action: 
    // Background/popup communication
    | 'CAPTURE_CONTENT'
    | 'CONTENT_CAPTURED'
    | 'SEND_TO_API'
    | 'API_RESPONSE'
    | 'GET_SETTINGS'
    | 'UPDATE_SETTINGS'
    // Content script communication
    | 'getSelectedText'
    | 'getPageContent'
    | 'getChatContent';
  payload?: any;
} 