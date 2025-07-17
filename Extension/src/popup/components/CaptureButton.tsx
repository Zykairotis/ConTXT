import React from 'react';
import { CapturedContent } from '../../types';

interface CaptureButtonProps {
  type: 'page' | 'selection' | 'element';
  onCapture: (content: CapturedContent) => void;
  disabled?: boolean;
}

const CaptureButton: React.FC<CaptureButtonProps> = ({
  type,
  onCapture,
  disabled = false,
}) => {
  const handleClick = async () => {
    try {
      // This is a placeholder - actual implementation would depend on the contentCapture service
      const content: CapturedContent = {
        type: 'html',
        content: '<p>Sample captured content</p>',
        metadata: {
          url: 'https://example.com',
          title: 'Example Page',
          timestamp: Date.now(),
          source: 'browser-extension',
        },
      };
      
      onCapture(content);
    } catch (error) {
      console.error('Error capturing content:', error);
    }
  };

  const getButtonText = () => {
    switch (type) {
      case 'page':
        return 'Capture Page';
      case 'selection':
        return 'Capture Selection';
      case 'element':
        return 'Capture Element';
      default:
        return 'Capture';
    }
  };

  return (
    <button
      className={`capture-button capture-button--${type}`}
      onClick={handleClick}
      disabled={disabled}
    >
      {getButtonText()}
    </button>
  );
};

export default CaptureButton; 