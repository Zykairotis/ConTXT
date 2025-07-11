# Frontend Documentation

## Project Role

The frontend is the user-facing interface for the **AI Context Builder**. It provides an intuitive, responsive, and efficient web application for users to upload, manage, and process data from various sources. Its primary goal is to abstract the complexity of the backend processing pipelines and present the results—the generated system prompts and configuration rules—in a clear and interactive manner.

## Core Responsibilities

1.  **Component Development:** Build, maintain, and enhance reusable UI components using React, TypeScript, and `shadcn/ui`.
2.  **State Management:** Implement robust client-side state management for handling complex application data, including uploaded files, real-time processing status, and the final generated context.
3.  **API Integration:** Connect seamlessly to the FastAPI backend. This includes handling asynchronous data fetching, submitting data for processing, and managing all API states (loading, success, error) gracefully.
4.  **User Experience (UX):** Design and implement a clean and intuitive user interface that simplifies the context-building workflow. The UI should be fully responsive and accessible.

## Tech Stack & Conventions

*   **Framework:** Next.js (using the App Router)
*   **Language:** TypeScript
*   **Styling:** Tailwind CSS
*   **UI Components:** `shadcn/ui`. Adherence to its design patterns and composition principles is required.
*   **Hooks:** Utilize custom hooks like `use-toast` and `use-mobile` for shared, reusable logic.
*   **File Structure:** Maintain the existing project structure, placing new components, hooks, and utilities in their designated directories (`/components`, `/hooks`, `/lib`).
*   **Code Quality:** All code must be clean, well-documented, and strongly-typed.

## Key Application Components

*   **`FileUpload`:** A component for uploading various document types (`pdf`, `json`, `md`, etc.).
*   **`WebUrlInput`:** An input field for submitting URLs for scraping and analysis.
*   **`VideoProcessor`:** A component to handle video file uploads (`mp4`, `mkv`) and YouTube links.
*   **`ContextViewer`:** A sophisticated view to display the aggregated and processed context from all sources in a clear, organized manner.
*   **`SystemPromptGenerator`:** An interactive text area where the generated system prompt is displayed, allowing the user to review, edit, and approve it.
*   **`ProjectContextBuilder`:** The main dashboard or orchestrator component that integrates all other parts of the UI, managing the overall state of a context-building session.

## Getting Started

1.  Navigate to the `Frontend` directory:
    ```bash
    cd Frontend
    ```
2.  Install the required dependencies:
    ```bash
    pnpm install
    ```
3.  Run the development server:
    ```bash
    pnpm run dev
    ```
4.  Open [http://localhost:3000](http://localhost:3000) in your browser.
