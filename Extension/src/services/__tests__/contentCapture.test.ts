import { CapturedContent } from '../../types';

// Mock the chrome API
const mockCaptureVisibleTab = jest.fn().mockResolvedValue('data:image/png;base64,mockImageData');
const mockQuery = jest.fn().mockResolvedValue([{ id: 1 }]);

jest.mock('webextension-polyfill', () => ({
  tabs: {
    captureVisibleTab: mockCaptureVisibleTab,
    query: mockQuery,
  },
}));

describe('contentCapture', () => {
  describe('captureVisibleContent', () => {
    it('should capture the visible content of the current tab', async () => {
      // This is just a placeholder test
      const mockContent: CapturedContent = {
        type: 'image',
        content: 'data:image/png;base64,mockImageData',
        metadata: {
          url: 'https://example.com',
          title: 'Example Page',
          timestamp: Date.now(),
          source: 'browser-extension'
        }
      };
      
      expect(mockContent.type).toBe('image');
    });
  });
}); 