import { CapturedContent } from '../types';

/**
 * Generate a unique ID for content items
 */
export const generateId = (): string => {
  return Date.now().toString(36) + Math.random().toString(36).substring(2);
};

/**
 * Format a date for display
 */
export const formatDate = (timestamp: number): string => {
  return new Date(timestamp).toLocaleString();
};

/**
 * Truncate text to a specific length
 */
export const truncateText = (text: string, maxLength: number = 100): string => {
  if (text.length <= maxLength) return text;
  return text.substring(0, maxLength) + '...';
};

/**
 * Extract the domain from a URL
 */
export const extractDomain = (url: string): string => {
  try {
    const urlObj = new URL(url);
    return urlObj.hostname;
  } catch (error) {
    return '';
  }
};

/**
 * Detect content type from a string
 */
export const detectContentType = (content: string): CapturedContent['type'] => {
  if (content.startsWith('data:image')) return 'image';
  if (content.startsWith('data:application/pdf')) return 'pdf';
  if (content.startsWith('<!DOCTYPE html>') || content.includes('<html')) return 'html';
  if (content.startsWith('http')) return 'url';
  return 'text';
}; 