import browser from 'webextension-polyfill';
import { Message } from '../types';

/**
 * Content script for the ConTXT Browser Extension
 * 
 * This script runs in the context of web pages and handles:
 * - Text selection capture
 * - Page content capture
 * - Chat content detection and capture
 * - DOM element selection
 */

// Listen for messages from the background script or popup
browser.runtime.onMessage.addListener((message: Message): any => {
  try {
    const { action } = message;
    
    switch (action) {
      case 'getSelectedText':
        return Promise.resolve({
          text: window.getSelection()?.toString() || '',
        });
      
      case 'getPageContent':
        return Promise.resolve({
          html: document.documentElement.outerHTML,
        });
      
      case 'getChatContent':
        return Promise.resolve(detectAndCaptureChatContent());
      
      default:
        return Promise.resolve({ error: `Unknown action: ${action}` });
    }
  } catch (error: any) {
    console.error('Error in content script:', error);
    return Promise.resolve({ error: error.message || 'Unknown error' });
  }
});

/**
 * Detect and capture chat content from supported platforms
 */
function detectAndCaptureChatContent(): { platform: string; content: string; title: string; error?: string } {
  // Helper function to detect platform
  const detectPlatform = (): string => {
    const url = window.location.href;
    if (url.includes('chat.openai.com')) return 'chatgpt';
    if (url.includes('claude.ai')) return 'claude';
    if (url.includes('gemini.google.com')) return 'gemini';
    if (url.includes('grok.x.ai')) return 'grok';
    return 'unknown';
  };
  
  const platform = detectPlatform();
  
  // Platform-specific selectors
  const selectors: Record<string, string> = {
    'chatgpt': '.markdown',
    'claude': '.claude-part',
    'gemini': '.gemini-response',
    'grok': '.grok-message',
    'unknown': '',
  };
  
  // Get chat elements
  const selector = selectors[platform];
  if (!selector) {
    return { 
      platform, 
      content: '', 
      title: document.title,
      error: 'Unsupported platform' 
    };
  }
  
  const chatElements = Array.from(document.querySelectorAll(selector));
  const chatContent = chatElements.map(el => el.textContent).join('\n\n');
  
  return {
    platform,
    content: chatContent,
    title: document.title,
  };
}

// Add a small visual indicator when the extension is active
function addExtensionIndicator() {
  const indicator = document.createElement('div');
  indicator.style.position = 'fixed';
  indicator.style.bottom = '10px';
  indicator.style.right = '10px';
  indicator.style.width = '10px';
  indicator.style.height = '10px';
  indicator.style.borderRadius = '50%';
  indicator.style.backgroundColor = '#4285F4';
  indicator.style.zIndex = '9999';
  indicator.style.opacity = '0.7';
  indicator.title = 'ConTXT Browser Extension Active';
  
  document.body.appendChild(indicator);
  
  // Remove after 3 seconds
  setTimeout(() => {
    indicator.style.transition = 'opacity 1s ease-out';
    indicator.style.opacity = '0';
    setTimeout(() => indicator.remove(), 1000);
  }, 3000);
}

// Initialize
(function init() {
  // Add the indicator when the content script loads
  if (document.readyState === 'complete') {
    addExtensionIndicator();
  } else {
    window.addEventListener('load', addExtensionIndicator);
  }
})(); 