// Environment detection
declare const process: {
  env: {
    NODE_ENV?: string;
  };
};

const isDevelopment = process.env.NODE_ENV === 'development';

// Configuration object
const config = {
  // API configuration
  api: {
    baseUrl: isDevelopment
      ? 'http://localhost:8000'
      : 'https://api.contxt.ai',
    timeout: 30000, // 30 seconds
  },
  
  // Extension settings
  extension: {
    name: 'ConTXT Browser Extension',
    version: '0.1.0',
    debug: isDevelopment,
  },
  
  // Storage settings
  storage: {
    // Maximum number of items to store in history
    maxHistoryItems: 100,
    // Use sync storage for settings, local storage for content
    useSync: true,
  },
};

export default config; 