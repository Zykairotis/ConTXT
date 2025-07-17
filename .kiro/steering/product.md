# AI Context Engineering Agent

## Product Overview
The AI Context Engineering Agent is a specialized system that curates optimal context for AI-driven software development. It focuses on deliberate context curation to fit within LLM context windows while maximizing relevance and utility.

## Core Purpose
- **Context Curation**: Transform raw data sources into precise, compressed context for AI agents
- **Multi-source Ingestion**: Process documents, chats, videos, URLs, and other data sources
- **Tool Integration**: Generate tailored prompts and rules for AI coding tools (Cursor, Windsurf, Gemini CLI)
- **Deployment Ready**: Bundle as Docker containers for easy sharing and deployment

## Key Features
- Multi-modal data ingestion with processors for various content types
- Context analysis engine using LangGraph workflows
- Knowledge graph storage (Neo4j) and vector search (Qdrant)
- Context compression and ordering to prevent LLM overload
- Tool-specific prompt and rule generation
- Docker-based deployment bundling

## Target Users
- Developers using AI coding assistants
- Teams needing consistent AI behavior across projects
- AI researchers experimenting with agent workflows
- Organizations requiring scalable, verifiable AI agents

## Success Metrics
- Context quality score >85% (relevance-based)
- AI tool accuracy improvement >50% from baseline
- Generation time <3 minutes for context curation
- 99% service uptime for production deployments