# ConTXT Browser Extension Architecture

This document outlines the architecture of the ConTXT browser extension, which enables users to capture and send web content to the ConTXT AI Context Engineering Agent.

## Overview

The extension is built using modern web technologies and follows a modular architecture to ensure maintainability and extensibility. It uses TypeScript for type safety and React for the popup UI.

## Components

### 1. Core Services

- **ApiService**: Communicates with the ConTXT backend FastAPI server
- **StorageService**: Manages extension settings and cached data
- **ContentCaptureService**: Handles capturing different types of web content
- **IngestionService**: Coordinates between content capture and API services

### 2. Extension Components

- **Background Script**: Handles context menu actions, messaging, and background tasks
- **Content Script**: Runs in the context of web pages to interact with page content
- **Popup UI**: User interface for capturing content and configuring settings

## Data Flow

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│    User Input   │────▶│   Popup UI      │────▶│  Background     │
│                 │     │                 │     │  Script         │
└─────────────────┘     └─────────────────┘     └────────┬────────┘
                                                         │
                                                         ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│  Content Script │◀────│ Ingestion       │◀────│ Content         │
│                 │     │ Service         │     │ Capture Service │
└────────┬────────┘     └────────┬────────┘     └─────────────────┘
         │                       │
         │                       ▼
         │              ┌─────────────────┐     ┌─────────────────┐
         │              │                 │     │                 │
         └─────────────▶│   API Service   │────▶│ ConTXT Backend  │
                        │                 │     │                 │
                        └─────────────────┘     └─────────────────┘
```

## Content Capture Flow

1. User initiates content capture (via popup UI or context menu)
2. Background script receives the request
3. Content capture service extracts the requested content
4. Ingestion service processes and prepares the content
5. API service sends the content to the ConTXT backend
6. Response is returned to the user with job ID for tracking

## Supported Content Types

- **URL**: Captures and processes the current URL
- **Text**: Captures selected text from the current page
- **Screenshot**: Captures a screenshot of the visible area or full page
- **HTML**: Captures the HTML content of the current page
- **Chat**: Detects and captures chat content from supported platforms
- **File**: Uploads files (PDF, images, etc.) to the backend

## Storage

The extension uses browser storage to persist:

- User settings (API URL, capture options)
- Job tracking information
- Cached data for performance optimization

## Communication

- **Background to Content Script**: Uses `browser.tabs.sendMessage`
- **Content Script to Background**: Uses `browser.runtime.sendMessage`
- **Popup to Background**: Uses `browser.runtime.sendMessage`
- **Extension to Backend**: Uses `fetch` API with appropriate headers

## Security Considerations

- The extension requests only the permissions it needs
- API keys and sensitive data are stored securely
- Content is processed locally before being sent to the backend
- User is always in control of what content is captured and sent

## Development and Build Process

The extension is built using:

- TypeScript for type safety
- React for the popup UI
- Webpack for bundling
- ESLint and Prettier for code quality
- Jest for testing

## Deployment

The extension can be packaged and deployed to:

- Chrome Web Store
- Firefox Add-ons Store

## Future Enhancements

- Support for additional content types
- Enhanced chat platform integration
- Offline processing capabilities
- Advanced content selection tools 