# AI Context Builder Documentation

This document provides a comprehensive overview of the AI Context Builder application, including its architecture, features, and usage.

## 1. Project Overview

The AI Context Builder is a full-stack application designed to streamline the process of creating and managing context for AI applications. It allows users to ingest data from various sources, generate system prompts, and configure rules for different AI development environments.

**Key Features:**

*   **Multi-Source Data Ingestion:** Supports data from URLs, files, and videos.
*   **AI-Powered Analysis:** Leverages AI to analyze libraries and improve text.
*   **System Prompt Generation:** Automatically generates tailored system prompts.
*   **Context Building:** Consolidates all data into a comprehensive context document.
*   **Rule Configuration:** Allows users to define rules and constraints for AI tools.

## 2. Architecture

The application follows a client-server architecture:

*   **Frontend:** A Next.js application responsible for the user interface and client-side logic.
*   **Backend:** A Python-based backend (not yet implemented) that will handle data processing and AI-related tasks.

## 3. Frontend

The frontend is built with Next.js, TypeScript, and Tailwind CSS. It uses `shadcn/ui` for UI components.

### 3.1. API Routes

The frontend includes several API routes to handle communication with the backend and external services:

*   **/api/analyze-library**: Analyzes a given library to extract its main purpose, features, use cases, and best practices.
*   **/api/build-context**: Builds a comprehensive context document from various sources like URLs, files, chat logs, and more.
*   **/api/generate-system-prompt**: Generates a system prompt for an LLM used in software development.
*   **/api/improve-text**: Enhances a given text by improving its clarity, structure, and grammar.
*   **/api/process-url**: Fetches and extracts content from a given URL.
*   **/api/process-video**: Transcribes a video from a URL or file, providing real-time progress updates.
*   **/api/whisper-transcribe**: Transcribes an audio URL using a mock Whisper API.

### 3.2. UI Components

The user interface is composed of several React components:

*   **ContextViewer:** Displays the generated context and allows users to copy or download it.
*   **FileUpload:** Enables users to upload files in various formats.
*   **LibraryAnalyzer:** Allows users to analyze libraries and their functionalities.
*   **ProjectContextBuilder:** Provides a form for defining project context, rules, and tool requirements.
*   **SystemPromptGenerator:** Generates and displays a system prompt.
*   **VideoProcessor:** Handles the processing of videos from URLs or files.
*   **WebUrlInput:** Allows users to add web URLs for content extraction.

## 4. Backend

(This section will be updated once the backend is implemented.)

## 5. Getting Started

(This section will be updated with instructions on how to set up and run the project.)
