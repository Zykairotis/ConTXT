import React, { useEffect, useState } from 'react';
import ReactDOM from 'react-dom/client';
import browser from 'webextension-polyfill';
import { StorageService, Settings } from '../services/storage';

import './popup.css';

interface CaptureOptions {
  includeMetadata: boolean;
  captureScreenshot: boolean;
  captureFullPage: boolean;
  captureSelection: boolean;
  captureChat: boolean;
}

interface StatusMessage {
  type: 'success' | 'error' | null;
  message: string;
}

const Popup: React.FC = () => {
  const [settings, setSettings] = useState<Settings | null>(null);
  const [status, setStatus] = useState<StatusMessage>({ type: null, message: '' });
  const [isProcessing, setIsProcessing] = useState(false);
  
  const storageService = new StorageService();
  
  useEffect(() => {
    // Load settings when popup opens
    const loadSettings = async () => {
      try {
        const settings = await storageService.getSettings();
        setSettings(settings);
        
        // Update API URL input
        const apiUrlInput = document.getElementById('api-url') as HTMLInputElement;
        if (apiUrlInput) {
          apiUrlInput.value = settings.apiUrl;
        }
        
        // Update checkboxes
        const includeMetadataCheckbox = document.getElementById('include-metadata') as HTMLInputElement;
        if (includeMetadataCheckbox) {
          includeMetadataCheckbox.checked = settings.captureOptions.includeMetadata;
        }
        
        const fullPageScreenshotCheckbox = document.getElementById('full-page-screenshot') as HTMLInputElement;
        if (fullPageScreenshotCheckbox) {
          fullPageScreenshotCheckbox.checked = settings.captureOptions.captureFullPage;
        }
      } catch (error) {
        console.error('Error loading settings:', error);
        setStatus({
          type: 'error',
          message: 'Failed to load settings',
        });
      }
    };
    
    loadSettings();
    
    // Set up event listeners
    setupEventListeners();
    
    return () => {
      // Clean up event listeners
      cleanupEventListeners();
    };
  }, []);
  
  const setupEventListeners = () => {
    // Capture URL button
    const captureUrlButton = document.getElementById('capture-url');
    if (captureUrlButton) {
      captureUrlButton.addEventListener('click', handleCaptureUrl);
    }
    
    // Capture text button
    const captureTextButton = document.getElementById('capture-text');
    if (captureTextButton) {
      captureTextButton.addEventListener('click', handleCaptureText);
    }
    
    // Capture screenshot button
    const captureScreenshotButton = document.getElementById('capture-screenshot');
    if (captureScreenshotButton) {
      captureScreenshotButton.addEventListener('click', handleCaptureScreenshot);
    }
    
    // Capture chat button
    const captureChatButton = document.getElementById('capture-chat');
    if (captureChatButton) {
      captureChatButton.addEventListener('click', handleCaptureChat);
    }
    
    // File upload
    const fileUpload = document.getElementById('file-upload');
    const fileInput = document.getElementById('file-input') as HTMLInputElement;
    
    if (fileUpload && fileInput) {
      fileUpload.addEventListener('click', () => {
        fileInput.click();
      });
      
      fileInput.addEventListener('change', handleFileUpload);
      
      // Drag and drop
      fileUpload.addEventListener('dragover', (e) => {
        e.preventDefault();
        fileUpload.classList.add('active');
      });
      
      fileUpload.addEventListener('dragleave', () => {
        fileUpload.classList.remove('active');
      });
      
      fileUpload.addEventListener('drop', (e: DragEvent) => {
        e.preventDefault();
        fileUpload.classList.remove('active');
        
        if (e.dataTransfer && e.dataTransfer.files.length > 0) {
          handleFileUpload({ target: { files: e.dataTransfer.files } } as any);
        }
      });
    }
    
    // Settings changes
    const apiUrlInput = document.getElementById('api-url') as HTMLInputElement;
    if (apiUrlInput) {
      apiUrlInput.addEventListener('change', handleApiUrlChange);
    }
    
    const includeMetadataCheckbox = document.getElementById('include-metadata') as HTMLInputElement;
    if (includeMetadataCheckbox) {
      includeMetadataCheckbox.addEventListener('change', handleIncludeMetadataChange);
    }
    
    const fullPageScreenshotCheckbox = document.getElementById('full-page-screenshot') as HTMLInputElement;
    if (fullPageScreenshotCheckbox) {
      fullPageScreenshotCheckbox.addEventListener('change', handleFullPageScreenshotChange);
    }
  };
  
  const cleanupEventListeners = () => {
    // Remove event listeners to prevent memory leaks
    const captureUrlButton = document.getElementById('capture-url');
    if (captureUrlButton) {
      captureUrlButton.removeEventListener('click', handleCaptureUrl);
    }
    
    const captureTextButton = document.getElementById('capture-text');
    if (captureTextButton) {
      captureTextButton.removeEventListener('click', handleCaptureText);
    }
    
    const captureScreenshotButton = document.getElementById('capture-screenshot');
    if (captureScreenshotButton) {
      captureScreenshotButton.removeEventListener('click', handleCaptureScreenshot);
    }
    
    const captureChatButton = document.getElementById('capture-chat');
    if (captureChatButton) {
      captureChatButton.removeEventListener('click', handleCaptureChat);
    }
    
    // File upload
    const fileUpload = document.getElementById('file-upload');
    const fileInput = document.getElementById('file-input') as HTMLInputElement;
    
    if (fileUpload && fileInput) {
      fileUpload.removeEventListener('click', () => {
        fileInput.click();
      });
      
      fileInput.removeEventListener('change', handleFileUpload);
    }
    
    // Settings changes
    const apiUrlInput = document.getElementById('api-url') as HTMLInputElement;
    if (apiUrlInput) {
      apiUrlInput.removeEventListener('change', handleApiUrlChange);
    }
    
    const includeMetadataCheckbox = document.getElementById('include-metadata') as HTMLInputElement;
    if (includeMetadataCheckbox) {
      includeMetadataCheckbox.removeEventListener('change', handleIncludeMetadataChange);
    }
    
    const fullPageScreenshotCheckbox = document.getElementById('full-page-screenshot') as HTMLInputElement;
    if (fullPageScreenshotCheckbox) {
      fullPageScreenshotCheckbox.removeEventListener('change', handleFullPageScreenshotChange);
    }
  };
  
  const getCaptureOptions = (): CaptureOptions => {
    const includeMetadataCheckbox = document.getElementById('include-metadata') as HTMLInputElement;
    const fullPageScreenshotCheckbox = document.getElementById('full-page-screenshot') as HTMLInputElement;
    
    return {
      includeMetadata: includeMetadataCheckbox?.checked ?? true,
      captureScreenshot: false,
      captureFullPage: fullPageScreenshotCheckbox?.checked ?? false,
      captureSelection: false,
      captureChat: false,
    };
  };
  
  const handleCaptureUrl = async () => {
    if (isProcessing) return;
    
    setIsProcessing(true);
    setStatus({ type: null, message: '' });
    
    try {
      const options = getCaptureOptions();
      
      const response = await browser.runtime.sendMessage({
        action: 'ingestUrl',
        data: { options },
      });
      
      if (response.error) {
        throw new Error(response.error);
      }
      
      setStatus({
        type: 'success',
        message: `URL sent to ConTXT (Job ID: ${response.jobId})`,
      });
    } catch (error) {
      console.error('Error capturing URL:', error);
      setStatus({
        type: 'error',
        message: `Failed to capture URL: ${(error as Error).message}`,
      });
    } finally {
      setIsProcessing(false);
    }
  };
  
  const handleCaptureText = async () => {
    if (isProcessing) return;
    
    setIsProcessing(true);
    setStatus({ type: null, message: '' });
    
    try {
      const options = getCaptureOptions();
      options.captureSelection = true;
      
      const response = await browser.runtime.sendMessage({
        action: 'ingestText',
        data: { options },
      });
      
      if (response.error) {
        throw new Error(response.error);
      }
      
      setStatus({
        type: 'success',
        message: `Selected text sent to ConTXT (Job ID: ${response.jobId})`,
      });
    } catch (error) {
      console.error('Error capturing text:', error);
      setStatus({
        type: 'error',
        message: `Failed to capture text: ${(error as Error).message}`,
      });
    } finally {
      setIsProcessing(false);
    }
  };
  
  const handleCaptureScreenshot = async () => {
    if (isProcessing) return;
    
    setIsProcessing(true);
    setStatus({ type: null, message: '' });
    
    try {
      const options = getCaptureOptions();
      options.captureScreenshot = true;
      
      const response = await browser.runtime.sendMessage({
        action: 'ingestScreenshot',
        data: { options },
      });
      
      if (response.error) {
        throw new Error(response.error);
      }
      
      setStatus({
        type: 'success',
        message: `Screenshot sent to ConTXT (Job ID: ${response.jobId})`,
      });
    } catch (error) {
      console.error('Error capturing screenshot:', error);
      setStatus({
        type: 'error',
        message: `Failed to capture screenshot: ${(error as Error).message}`,
      });
    } finally {
      setIsProcessing(false);
    }
  };
  
  const handleCaptureChat = async () => {
    if (isProcessing) return;
    
    setIsProcessing(true);
    setStatus({ type: null, message: '' });
    
    try {
      const options = getCaptureOptions();
      options.captureChat = true;
      
      const response = await browser.runtime.sendMessage({
        action: 'ingestChat',
        data: { options },
      });
      
      if (response.error) {
        throw new Error(response.error);
      }
      
      setStatus({
        type: 'success',
        message: `Chat content sent to ConTXT (Job ID: ${response.jobId})`,
      });
    } catch (error) {
      console.error('Error capturing chat:', error);
      setStatus({
        type: 'error',
        message: `Failed to capture chat: ${(error as Error).message}`,
      });
    } finally {
      setIsProcessing(false);
    }
  };
  
  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    if (isProcessing) return;
    
    const fileInput = event.target as HTMLInputElement;
    const files = fileInput.files;
    
    if (!files || files.length === 0) {
      return;
    }
    
    setIsProcessing(true);
    setStatus({ type: null, message: '' });
    
    try {
      const file = files[0];
      const options = getCaptureOptions();
      
      // Create a FormData object
      const formData = new FormData();
      formData.append('file', file);
      
      // Get the active tab
      const tabs = await browser.tabs.query({ active: true, currentWindow: true });
      const currentTab = tabs[0];
      
      // Add metadata
      if (options.includeMetadata && currentTab.url) {
        const metadata = {
          sourceUrl: currentTab.url,
          sourceTitle: currentTab.title,
          timestamp: new Date().toISOString(),
        };
        
        formData.append('metadata', JSON.stringify(metadata));
      }
      
      // Send the file to the background script
      const response = await fetch(`${settings?.apiUrl}/ingestion/file`, {
        method: 'POST',
        body: formData,
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error ${response.status}`);
      }
      
      const data = await response.json();
      
      setStatus({
        type: 'success',
        message: `File "${file.name}" sent to ConTXT (Job ID: ${data.job_id})`,
      });
      
      // Clear the file input
      fileInput.value = '';
    } catch (error) {
      console.error('Error uploading file:', error);
      setStatus({
        type: 'error',
        message: `Failed to upload file: ${(error as Error).message}`,
      });
    } finally {
      setIsProcessing(false);
    }
  };
  
  const handleApiUrlChange = async (event: Event) => {
    const input = event.target as HTMLInputElement;
    const apiUrl = input.value.trim();
    
    try {
      await storageService.saveSettings({ apiUrl });
      setStatus({
        type: 'success',
        message: 'API URL updated',
      });
      
      // Update settings state
      setSettings(await storageService.getSettings());
      
      // Clear status after 2 seconds
      setTimeout(() => {
        setStatus({ type: null, message: '' });
      }, 2000);
    } catch (error) {
      console.error('Error saving API URL:', error);
      setStatus({
        type: 'error',
        message: 'Failed to save API URL',
      });
    }
  };
  
  const handleIncludeMetadataChange = async (event: Event) => {
    const checkbox = event.target as HTMLInputElement;
    
    try {
      await storageService.saveSettings({
        captureOptions: {
          includeMetadata: checkbox.checked,
        },
      });
      
      // Update settings state
      setSettings(await storageService.getSettings());
    } catch (error) {
      console.error('Error saving include metadata setting:', error);
      setStatus({
        type: 'error',
        message: 'Failed to save settings',
      });
    }
  };
  
  const handleFullPageScreenshotChange = async (event: Event) => {
    const checkbox = event.target as HTMLInputElement;
    
    try {
      await storageService.saveSettings({
        captureOptions: {
          captureFullPage: checkbox.checked,
        },
      });
      
      // Update settings state
      setSettings(await storageService.getSettings());
    } catch (error) {
      console.error('Error saving full page screenshot setting:', error);
      setStatus({
        type: 'error',
        message: 'Failed to save settings',
      });
    }
  };
  
  return (
    <div id="status-container">
      {status.type && (
        <div className={`status ${status.type}`}>
          {status.message}
        </div>
      )}
    </div>
  );
};

// Create root and render the popup
const root = ReactDOM.createRoot(document.getElementById('status') as HTMLElement);
root.render(<Popup />); 