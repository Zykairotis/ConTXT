import browser from 'webextension-polyfill';
import { CapturedContent } from '../types';
import { CONTENT_TYPES } from '../constants';

/**
 * Capture options interface
 */
export interface CaptureOptions {
  includeMetadata?: boolean;
  captureScreenshot?: boolean;
  captureFullPage?: boolean;
}

/**
 * Capture the current URL
 * @returns The captured URL content
 */
export async function captureUrl(): Promise<CapturedContent> {
  try {
    const tabs = await browser.tabs.query({ active: true, currentWindow: true });
    const currentTab = tabs[0];
    
    if (!currentTab.url) {
      throw new Error('No URL found in the current tab');
    }
    
    return {
      type: 'url',
      content: currentTab.url,
      metadata: {
        url: currentTab.url,
        title: currentTab.title || 'Untitled',
        timestamp: Date.now(),
        source: 'browser-extension',
      },
    };
  } catch (error) {
    console.error('Error capturing URL:', error);
    throw error;
  }
}

/**
 * Capture a screenshot of the current tab
 * @param options Capture options
 * @returns The captured screenshot
 */
export async function captureVisibleContent(options: CaptureOptions = {}): Promise<CapturedContent> {
  try {
    const tabs = await browser.tabs.query({ active: true, currentWindow: true });
    const currentTab = tabs[0];
    
    if (!currentTab.id) {
      throw new Error('No tab ID found');
    }
    
    // Capture screenshot
    const dataUrl = await browser.tabs.captureVisibleTab();
    
    return {
      type: 'image',
      content: dataUrl,
      metadata: {
        url: currentTab.url || '',
        title: currentTab.title || 'Screenshot',
        timestamp: Date.now(),
        source: 'browser-extension',
      },
    };
  } catch (error) {
    console.error('Error capturing screenshot:', error);
    throw error;
  }
}

/**
 * Capture the selected text from the current tab
 * @returns The captured text
 */
export async function captureSelectedText(): Promise<CapturedContent> {
  try {
    const tabs = await browser.tabs.query({ active: true, currentWindow: true });
    const currentTab = tabs[0];
    
    if (!currentTab.id) {
      throw new Error('No tab ID found');
    }
    
    // Execute content script to get selected text
    const result = await browser.tabs.sendMessage(currentTab.id, { action: 'getSelectedText' });
    
    if (!result || !result.text) {
      throw new Error('No text selected');
    }
    
    return {
      type: 'text',
      content: result.text,
      metadata: {
        url: currentTab.url || '',
        title: currentTab.title || 'Selected Text',
        timestamp: Date.now(),
        source: 'browser-extension',
      },
    };
  } catch (error) {
    console.error('Error capturing selected text:', error);
    throw error;
  }
}

/**
 * Capture the HTML content of the current tab
 * @returns The captured HTML
 */
export async function capturePageContent(): Promise<CapturedContent> {
  try {
    const tabs = await browser.tabs.query({ active: true, currentWindow: true });
    const currentTab = tabs[0];
    
    if (!currentTab.id) {
      throw new Error('No tab ID found');
    }
    
    // Execute content script to get HTML
    const result = await browser.tabs.sendMessage(currentTab.id, { action: 'getPageContent' });
    
    if (!result || !result.html) {
      throw new Error('Failed to capture page content');
    }
    
    return {
      type: 'html',
      content: result.html,
      metadata: {
        url: currentTab.url || '',
        title: currentTab.title || 'HTML Content',
        timestamp: Date.now(),
        source: 'browser-extension',
      },
    };
  } catch (error) {
    console.error('Error capturing HTML content:', error);
    throw error;
  }
}

/**
 * Detect and capture chat content from supported platforms
 * @returns The captured chat content
 */
export async function captureChatContent(): Promise<CapturedContent> {
  try {
    const tabs = await browser.tabs.query({ active: true, currentWindow: true });
    const currentTab = tabs[0];
    
    if (!currentTab.id) {
      throw new Error('No tab ID found');
    }
    
    // Execute content script to detect and extract chat content
    const result = await browser.tabs.sendMessage(currentTab.id, { action: 'getChatContent' });
    
    if (!result || !result.content) {
      throw new Error(result?.error || 'Failed to capture chat content');
    }
    
    return {
      type: 'text',
      content: result.content,
      metadata: {
        url: currentTab.url || '',
        title: result.title || 'Chat Content',
        timestamp: Date.now(),
        source: `browser-extension-${result.platform}`,
      },
    };
  } catch (error) {
    console.error('Error capturing chat content:', error);
    throw error;
  }
} 