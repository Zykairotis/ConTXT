import browser from 'webextension-polyfill';
import { UserSettings, CapturedContent, StorageData } from '../types';
import { DEFAULT_SETTINGS, STORAGE_KEYS } from '../constants';

/**
 * Get the current user settings
 * @returns The current user settings
 */
export async function getSettings(): Promise<UserSettings> {
  try {
    const result = await browser.storage.local.get(STORAGE_KEYS.SETTINGS);
    return result[STORAGE_KEYS.SETTINGS] || DEFAULT_SETTINGS;
  } catch (error) {
    console.error('Error getting settings:', error);
    return DEFAULT_SETTINGS;
  }
}

/**
 * Save user settings
 * @param settings The settings to save
 */
export async function saveSettings(settings: UserSettings): Promise<void> {
  try {
    const data: Partial<StorageData> = {};
    data[STORAGE_KEYS.SETTINGS] = settings;
    await browser.storage.local.set(data);
  } catch (error) {
    console.error('Error saving settings:', error);
    throw new Error('Failed to save settings');
  }
}

/**
 * Get the API key
 * @returns The API key if set
 */
export async function getApiKey(): Promise<string | undefined> {
  try {
    const result = await browser.storage.local.get(STORAGE_KEYS.API_KEY);
    return result[STORAGE_KEYS.API_KEY];
  } catch (error) {
    console.error('Error getting API key:', error);
    return undefined;
  }
}

/**
 * Save the API key
 * @param apiKey The API key to save
 */
export async function saveApiKey(apiKey: string): Promise<void> {
  try {
    const data: Partial<StorageData> = {};
    data[STORAGE_KEYS.API_KEY] = apiKey;
    await browser.storage.local.set(data);
  } catch (error) {
    console.error('Error saving API key:', error);
    throw new Error('Failed to save API key');
  }
}

/**
 * Get the server URL
 * @returns The server URL if set
 */
export async function getServerUrl(): Promise<string | undefined> {
  try {
    const result = await browser.storage.local.get(STORAGE_KEYS.SERVER_URL);
    return result[STORAGE_KEYS.SERVER_URL];
  } catch (error) {
    console.error('Error getting server URL:', error);
    return undefined;
  }
}

/**
 * Save the server URL
 * @param serverUrl The server URL to save
 */
export async function saveServerUrl(serverUrl: string): Promise<void> {
  try {
    const data: Partial<StorageData> = {};
    data[STORAGE_KEYS.SERVER_URL] = serverUrl;
    await browser.storage.local.set(data);
  } catch (error) {
    console.error('Error saving server URL:', error);
    throw new Error('Failed to save server URL');
  }
}

/**
 * Get all captured content
 * @returns Array of captured content
 */
export async function getCapturedContent(): Promise<CapturedContent[]> {
  try {
    const result = await browser.storage.local.get(STORAGE_KEYS.CAPTURED_CONTENT);
    return result[STORAGE_KEYS.CAPTURED_CONTENT] || [];
  } catch (error) {
    console.error('Error getting captured content:', error);
    return [];
  }
}

/**
 * Save captured content
 * @param content The content to save
 */
export async function saveCapturedContent(content: CapturedContent): Promise<void> {
  try {
    const existingContent = await getCapturedContent();
    const updatedContent = [content, ...existingContent];
    
    const data: Partial<StorageData> = {};
    data[STORAGE_KEYS.CAPTURED_CONTENT] = updatedContent;
    await browser.storage.local.set(data);
  } catch (error) {
    console.error('Error saving captured content:', error);
    throw new Error('Failed to save captured content');
  }
}

/**
 * Delete captured content by index
 * @param index The index of the content to delete
 */
export async function deleteCapturedContent(index: number): Promise<void> {
  try {
    const existingContent = await getCapturedContent();
    if (index >= 0 && index < existingContent.length) {
      existingContent.splice(index, 1);
      
      const data: Partial<StorageData> = {};
      data[STORAGE_KEYS.CAPTURED_CONTENT] = existingContent;
      await browser.storage.local.set(data);
    }
  } catch (error) {
    console.error('Error deleting captured content:', error);
    throw new Error('Failed to delete captured content');
  }
}

/**
 * Clear all captured content
 */
export async function clearCapturedContent(): Promise<void> {
  try {
    const data: Partial<StorageData> = {};
    data[STORAGE_KEYS.CAPTURED_CONTENT] = [];
    await browser.storage.local.set(data);
  } catch (error) {
    console.error('Error clearing captured content:', error);
    throw new Error('Failed to clear captured content');
  }
} 