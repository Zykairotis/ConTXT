import browser from 'webextension-polyfill';
import * as ingestion from '../services/ingestion';
import * as storage from '../services/storage';
import { CONTEXT_MENU_IDS } from '../constants';
import { Message } from '../types';

// Initialize context menus when the extension is installed or updated
browser.runtime.onInstalled.addListener(() => {
  // Create context menu items
  browser.contextMenus.create({
    id: CONTEXT_MENU_IDS.CAPTURE_SELECTION,
    title: 'Send selected text to ConTXT',
    contexts: ['selection'],
  });

  browser.contextMenus.create({
    id: CONTEXT_MENU_IDS.CAPTURE_LINK,
    title: 'Send link to ConTXT',
    contexts: ['link'],
  });

  browser.contextMenus.create({
    id: CONTEXT_MENU_IDS.CAPTURE_IMAGE,
    title: 'Send image to ConTXT',
    contexts: ['image'],
  });

  browser.contextMenus.create({
    id: CONTEXT_MENU_IDS.CAPTURE_PAGE,
    title: 'Send page to ConTXT',
    contexts: ['page'],
  });
});

// Handle context menu clicks
browser.contextMenus.onClicked.addListener(async (info, tab) => {
  try {
    let result;
    
    switch (info.menuItemId) {
      case CONTEXT_MENU_IDS.CAPTURE_SELECTION:
        if (info.selectionText) {
          result = await ingestion.ingestSelectedText();
        }
        break;
        
      case CONTEXT_MENU_IDS.CAPTURE_LINK:
        if (info.linkUrl) {
          // For link captures, we need to navigate to the URL first
          // This is a simplified version - in a real extension, you might want to
          // fetch the content without navigating
          await browser.tabs.create({ url: info.linkUrl, active: false });
          result = await ingestion.ingestCurrentUrl();
        }
        break;
        
      case CONTEXT_MENU_IDS.CAPTURE_IMAGE:
        if (info.srcUrl) {
          // For image captures, we would need a special handler
          // This is simplified - in a real extension, you would download and process the image
          result = {
            success: false,
            contentType: 'image',
            timestamp: Date.now(),
            error: 'Direct image capture not implemented yet',
          };
        }
        break;
        
      case CONTEXT_MENU_IDS.CAPTURE_PAGE:
        if (tab?.url) {
          result = await ingestion.ingestCurrentUrl();
        }
        break;
    }
    
    if (result) {
      // Notify user of success or failure
      browser.notifications.create({
        type: 'basic',
        iconUrl: browser.runtime.getURL('assets/icon-48.png'),
        title: result.success ? 'ConTXT' : 'ConTXT Error',
        message: result.success 
          ? `Content sent to ConTXT${result.jobId ? ` (Job ID: ${result.jobId})` : ''}`
          : `Failed to send content: ${result.error}`,
      });
    }
  } catch (error: any) {
    console.error('Error handling context menu click:', error);
    
    // Notify user of error
    browser.notifications.create({
      type: 'basic',
      iconUrl: browser.runtime.getURL('assets/icon-48.png'),
      title: 'ConTXT Error',
      message: `Failed to send content: ${error.message || 'Unknown error'}`,
    });
  }
});

// Handle messages from popup or content scripts
browser.runtime.onMessage.addListener(async (message: Message, sender): Promise<any> => {
  try {
    const { action, payload } = message;
    
    switch (action) {
      case 'CAPTURE_CONTENT':
        switch (payload?.type) {
          case 'url':
            return await ingestion.ingestCurrentUrl();
          case 'text':
            return await ingestion.ingestSelectedText();
          case 'image':
            return await ingestion.ingestScreenshot();
          case 'html':
            return await ingestion.ingestPageContent();
          default:
            throw new Error(`Unknown content type: ${payload?.type}`);
        }
        
      case 'SEND_TO_API':
        if (payload?.jobId) {
          return await ingestion.checkStatus(payload.jobId);
        }
        throw new Error('No job ID provided');
        
      case 'GET_SETTINGS':
        return await storage.getSettings();
        
      case 'UPDATE_SETTINGS':
        if (payload) {
          await storage.saveSettings(payload);
          return { success: true };
        }
        throw new Error('No settings provided');
        
      default:
        throw new Error(`Unknown action: ${action}`);
    }
  } catch (error: any) {
    console.error('Error handling message:', error);
    return { success: false, error: error.message || 'Unknown error' };
  }
}); 