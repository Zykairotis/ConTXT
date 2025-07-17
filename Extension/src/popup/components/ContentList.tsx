import React from 'react';
import { CapturedContent } from '../../types';
import { formatDate, truncateText } from '../../utils';

interface ContentListProps {
  items: CapturedContent[];
  onSelect: (content: CapturedContent) => void;
  onDelete: (content: CapturedContent) => void;
}

const ContentList: React.FC<ContentListProps> = ({ items, onSelect, onDelete }) => {
  if (items.length === 0) {
    return (
      <div className="content-list content-list--empty">
        <p>No captured content yet.</p>
      </div>
    );
  }

  return (
    <div className="content-list">
      <h2>Captured Content</h2>
      <ul>
        {items.map((item, index) => (
          <li key={index} className={`content-item content-item--${item.type}`}>
            <div className="content-item__header">
              <span className="content-item__type">{item.type}</span>
              <span className="content-item__date">{formatDate(item.metadata.timestamp)}</span>
            </div>
            <div className="content-item__title" onClick={() => onSelect(item)}>
              {item.metadata.title || 'Untitled'}
            </div>
            <div className="content-item__preview">
              {item.type === 'image' ? (
                <img 
                  src={item.content} 
                  alt={item.metadata.title || 'Captured image'} 
                  className="content-item__image"
                />
              ) : (
                <p>{truncateText(item.content, 150)}</p>
              )}
            </div>
            <div className="content-item__actions">
              <button 
                className="btn-view" 
                onClick={() => onSelect(item)}
              >
                View
              </button>
              <button 
                className="btn-delete" 
                onClick={() => onDelete(item)}
              >
                Delete
              </button>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default ContentList; 