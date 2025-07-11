# Project Brief: AI Task Automation Platform

## 1. High-Level Vision

This project aims to build an AI Task Automation Platform. The platform will enable users to define and execute complex tasks by leveraging a suite of specialized AI agents. The system is designed to be highly extensible, allowing for the integration of new agents and tools over time.

## 2. Core Architecture

The system is composed of three main parts:

- **Frontend**: A web-based user interface for users to interact with the platform, manage tasks, and view results. Built with Next.js, React, and TypeScript.
- **Backend**: A FastAPI server that handles business logic, manages AI agent workflows, and serves the frontend.
- **AI Agents**: A collection of autonomous agents built with LangGraph, each specializing in a specific domain (e.g., Linux administration, programming).

## 3. Key Technologies

- **Frontend**: Next.js, React, TypeScript, Tailwind CSS, Radix UI
- **Backend**: FastAPI, Python
- **AI Orchestration**: LangGraph
- **Memory/State Management**: Graphiti with Neo4j
- **Infrastructure**: Docker, Supabase (for user auth and DB), Langfuse (for tracing)

## 4. Constraints & Considerations

- The system must be designed for scalability and extensibility.
- Security is a primary concern, especially regarding the execution of tasks by AI agents.
- The user experience should be intuitive and seamless, abstracting away the complexity of the underlying AI workflows.
