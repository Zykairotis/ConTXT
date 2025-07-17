# ConTXT Browser Extension

A browser extension for Chrome and Firefox that allows users to capture and send web content directly to the ConTXT AI Context Engineering Agent.

## Features

- Capture and process various web content types:
  - Text: Selected text from web pages
  - HTML: Full webpage content and structure
  - Images: Screenshots of visible content
  - URLs: Process web pages by URL
  - Chat: Extract conversations from AI chat platforms (ChatGPT, Claude, Gemini, Grok)

- Context menu integration for quick capture
- Popup interface for content management and settings
- Local storage for offline access to captured content
- Secure API communication with the ConTXT backend

## Architecture

The extension is built using a modern TypeScript architecture:

- **Background Script**: Handles context menus, browser events, and communication with the backend API
- **Content Script**: Runs in the context of web pages to interact with the DOM and capture content
- **Popup UI**: React-based interface for managing captured content and settings
- **Services**: Modular services for API communication, content capture, storage, and ingestion

## Development

This extension integrates with the ConTXT backend FastAPI server to process and store captured data in the knowledge graph and vector database.

### Prerequisites

- Node.js (v14+)
- npm or yarn
- Chrome or Firefox browser

### Installation

1. Clone the repository
2. Navigate to the Extension directory
3. Install dependencies:
   ```
   npm install
   ```
4. Build the extension:
   ```
   npm run build
   ```

### Development Mode

Run the extension in development mode with hot reloading:
```
npm run dev
```

### Loading the Extension

#### Chrome
1. Open chrome://extensions
2. Enable Developer mode
3. Click "Load unpacked"
4. Select the `dist` folder

#### Firefox
1. Open about:debugging
2. Click "This Firefox"
3. Click "Load Temporary Add-on"
4. Select any file in the `dist` folder

## Testing

Run the test suite:
```
npm test
```

## Building for Production

Build a production version of the extension:
```
npm run build
```

## Usage

1. Click the ConTXT extension icon in your browser
2. Select the type of content you want to capture
3. Configure capture options if needed
4. Click "Send to ConTXT" to process the captured content

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## License

MIT 