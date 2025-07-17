import { useState, useCallback } from 'react';
import { CapturedContent } from '../../types';
import browser from 'webextension-polyfill';

export const useCapture = () => {
  const [isCapturing, setIsCapturing] = useState(false);
  const [capturedContent, setCapturedContent] = useState<CapturedContent | null>(null);
  const [error, setError] = useState<string | null>(null);

  const captureCurrentPage = useCallback(async () => {
    try {
      setIsCapturing(true);
      setError(null);

      // Send message to background script to handle the capture
      const response = await browser.runtime.sendMessage({
        action: 'CAPTURE_CONTENT',
        payload: { type: 'page' }
      });

      if (response.success) {
        setCapturedContent(response.data);
      } else {
        setError(response.error || 'Failed to capture content');
      }
    } catch (err) {
      setError('An error occurred while capturing content');
      console.error(err);
    } finally {
      setIsCapturing(false);
    }
  }, []);

  const captureSelection = useCallback(async () => {
    try {
      setIsCapturing(true);
      setError(null);

      // Send message to background script to handle the capture
      const response = await browser.runtime.sendMessage({
        action: 'CAPTURE_CONTENT',
        payload: { type: 'selection' }
      });

      if (response.success) {
        setCapturedContent(response.data);
      } else {
        setError(response.error || 'Failed to capture selection');
      }
    } catch (err) {
      setError('An error occurred while capturing selection');
      console.error(err);
    } finally {
      setIsCapturing(false);
    }
  }, []);

  const clearCapture = useCallback(() => {
    setCapturedContent(null);
    setError(null);
  }, []);

  return {
    isCapturing,
    capturedContent,
    error,
    captureCurrentPage,
    captureSelection,
    clearCapture
  };
}; 