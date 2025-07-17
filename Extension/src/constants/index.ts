// API endpoints
export const API_BASE_URL = 'http://localhost:8000';
export const API_ENDPOINTS = {
  INGEST: '/api/ingest',
  PROCESS: '/api/process',
  STATUS: '/api/status',
};

// Storage keys
export const STORAGE_KEYS = {
  API_KEY: 'apiKey',
  SERVER_URL: 'serverUrl',
  SETTINGS: 'settings',
  CAPTURED_CONTENT: 'capturedContent',
};

// Default settings
export const DEFAULT_SETTINGS = {
  captureFormat: 'html',
  autoCapture: false,
  notificationsEnabled: true,
};

// Content types
export const CONTENT_TYPES = {
  TEXT: 'text',
  HTML: 'html',
  IMAGE: 'image',
  PDF: 'pdf',
  URL: 'url',
};

// Context menu IDs
export const CONTEXT_MENU_IDS = {
  CAPTURE_SELECTION: 'capture-selection',
  CAPTURE_PAGE: 'capture-page',
  CAPTURE_LINK: 'capture-link',
  CAPTURE_IMAGE: 'capture-image',
}; 