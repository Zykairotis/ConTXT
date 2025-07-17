import React, { useState, useEffect } from 'react';
import { UserSettings } from '../../types';
import { DEFAULT_SETTINGS } from '../../constants';
import * as storage from '../../services/storage';

interface SettingsPanelProps {
  onSave: (settings: UserSettings) => void;
}

const SettingsPanel: React.FC<SettingsPanelProps> = ({ onSave }) => {
  const [settings, setSettings] = useState<UserSettings>(DEFAULT_SETTINGS);

  useEffect(() => {
    const loadSettings = async () => {
      try {
        const savedSettings = await storage.getSettings();
        if (savedSettings) {
          setSettings(savedSettings);
        }
      } catch (error) {
        console.error('Failed to load settings:', error);
      }
    };

    loadSettings();
  }, []);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value, type } = e.target as HTMLInputElement;
    
    setSettings(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? (e.target as HTMLInputElement).checked : value
    }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSave(settings);
  };

  return (
    <div className="settings-panel">
      <h2>Settings</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="captureFormat">Default Capture Format:</label>
          <select 
            id="captureFormat" 
            name="captureFormat"
            value={settings.captureFormat}
            onChange={handleChange}
          >
            <option value="text">Plain Text</option>
            <option value="html">HTML</option>
            <option value="image">Screenshot</option>
          </select>
        </div>

        <div className="form-group">
          <label htmlFor="autoCapture">
            <input
              type="checkbox"
              id="autoCapture"
              name="autoCapture"
              checked={settings.autoCapture}
              onChange={handleChange}
            />
            Enable Auto-Capture
          </label>
        </div>

        <div className="form-group">
          <label htmlFor="notificationsEnabled">
            <input
              type="checkbox"
              id="notificationsEnabled"
              name="notificationsEnabled"
              checked={settings.notificationsEnabled}
              onChange={handleChange}
            />
            Enable Notifications
          </label>
        </div>

        <button type="submit" className="btn-save">
          Save Settings
        </button>
      </form>
    </div>
  );
};

export default SettingsPanel; 