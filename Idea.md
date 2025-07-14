The Idea Revolves Around making context System For the Ai Applications and using that context to make Better applications 
- Taking (Convo) Context from Sites 
	- Chatgpt
	- Claude
	- Grok
	- Gemini
	- Deepseek
	- Local Endpoint (Example Openwebui)
- Documents 
	- Pdf
	- Images
	- Json
	- Csv
	- Xml
	- Html
	- MD
	- PNG
	- URL
	- files in google drive if sharing is enabled
- Video Information 
	- Mp4 or Mkv
	- Youtube Video 

After getting this Initial Information from all the sources The Agent will make a System Prompt And u can improve it if you want to 
it will make Project Rule for all type of agents 
in the following manner 
- [ {gemini-cli,task,GEMINI.md},{cursor,task,GEMINI.md}, {Windsurf,task,GEMINI.md}]

Then it will give you the rules for files and patterns 
Examples : 
- File rules for cursor 
- File rules for Gemini
- File rules for Windsurf


# Tech Stack
Langgraph
langchain
Cognee
Markdown parser
Whisper
Docker
Tailwind 
TypeScript
Fast Api 


# LLM
# AI Context Builder Agent - Complete Project Documentation

## 🎯 Project Vision

Create an intelligent AI agent that automatically builds comprehensive context for AI applications by ingesting information from multiple sources, then generates tailored system prompts and rule configurations for various AI development environments.

## 🔥 Core Problem Statement

AI applications often lack proper context, resulting in generic responses and suboptimal performance. Developers spend significant time manually crafting system prompts and rules for different AI tools. This agent solves that by automatically building rich context from diverse sources and generating optimized configurations.

## 🚀 System Architecture

```mermaid
graph TB
    A[Input Sources] --> B[Context Ingestion Engine]
    B --> C[Knowledge Graph Builder]
    C --> D[System Prompt Generator]
    D --> E[Rules Engine]
    E --> F[Output Configurations]
    
    subgraph "Input Sources"
        A1[Chat Platforms]
        A2[Documents]
        A3[Media Files]
        A4[URLs]
    end
    
    subgraph "Output Configurations"
        F1[Gemini CLI Rules]
        F2[Cursor Rules]
        F3[Windsurf Rules]
        F4[System Prompts]
    end
```

## 📋 Feature Specifications

### 1. Multi-Source Context Ingestion

#### 1.1 Conversation Import System

```python
# Supported Chat Platforms
CHAT_PLATFORMS = {
    'chatgpt': {
        'export_format': 'json',
        'extraction_method': 'api_scraping',
        'auth_required': True
    },
    'claude': {
        'export_format': 'markdown',
        'extraction_method': 'browser_extension',
        'auth_required': True
    },
    'grok': {
        'export_format': 'html',
        'extraction_method': 'web_scraping',
        'auth_required': True
    },
    'gemini': {
        'export_format': 'json',
        'extraction_method': 'google_api',
        'auth_required': True
    },
    'deepseek': {
        'export_format': 'text',
        'extraction_method': 'web_scraping',
        'auth_required': True
    },
    'openwebui': {
        'export_format': 'json',
        'extraction_method': 'local_api',
        'auth_required': False
    }
}
```

#### 1.2 Document Processing Pipeline

```python
# Document Type Handlers
DOCUMENT_PROCESSORS = {
    'pdf': 'PyPDF2 + OCR fallback',
    'images': 'Vision API + OCR',
    'json': 'Schema analysis + content extraction',
    'csv': 'Pandas + semantic analysis',
    'xml': 'BeautifulSoup + structure parsing',
    'html': 'Content extraction + metadata',
    'md': 'Markdown parser + structure analysis',
    'png': 'Vision API + text extraction',
    'url': 'Web scraping + content analysis',
    'google_drive': 'Drive API + file processing'
}
```

#### 1.3 Video Information Extraction

```python
# Video Processing Capabilities
VIDEO_PROCESSORS = {
    'mp4': {
        'audio_extraction': 'Whisper API',
        'frame_analysis': 'Vision API',
        'subtitle_extraction': 'SRT parsing'
    },
    'mkv': {
        'audio_extraction': 'Whisper API',
        'frame_analysis': 'Vision API',
        'subtitle_extraction': 'SRT parsing'
    },
    'youtube': {
        'transcript_api': 'YouTube Data API',
        'audio_extraction': 'yt-dlp + Whisper',
        'metadata_extraction': 'YouTube API'
    }
}
```

### 2. Intelligent System Prompt Generation

#### 2.1 Context Analysis Engine

```python
class ContextAnalyzer:
    def __init__(self):
        self.domain_classifier = DomainClassifier()
        self.intent_analyzer = IntentAnalyzer()
        self.complexity_scorer = ComplexityScorer()
    
    def analyze_context(self, ingested_data):
        """
        Analyze all ingested data to understand:
        - Project domain (web dev, data science, etc.)
        - User intent and goals
        - Complexity level
        - Required capabilities
        """
        return {
            'domain': self.domain_classifier.classify(ingested_data),
            'intent': self.intent_analyzer.analyze(ingested_data),
            'complexity': self.complexity_scorer.score(ingested_data),
            'capabilities': self.extract_required_capabilities(ingested_data)
        }
```

#### 2.2 Dynamic Prompt Builder

```python
class SystemPromptGenerator:
    def generate_prompt(self, context_analysis, user_preferences):
        """
        Generate optimized system prompt based on:
        - Analyzed context
        - User preferences
        - Best practices for the target domain
        """
        prompt_template = self.select_base_template(context_analysis.domain)
        
        # Customize based on context
        customized_prompt = self.customize_for_context(
            prompt_template, 
            context_analysis
        )
        
        # Add user-specific preferences
        final_prompt = self.apply_user_preferences(
            customized_prompt, 
            user_preferences
        )
        
        return final_prompt
```

### 3. Rules Engine for AI Development Tools

#### 3.1 Rule Configuration System

```python
# Rule Templates for Different AI Tools
RULE_TEMPLATES = {
    'gemini_cli': {
        'file_patterns': [
            '*.py: Python files with type hints',
            '*.js: JavaScript with modern syntax',
            '*.md: Documentation files',
            '*.json: Configuration files'
        ],
        'behavior_rules': [
            'Always provide complete code examples',
            'Include error handling',
            'Follow PEP 8 for Python',
            'Use meaningful variable names'
        ],
        'context_rules': [
            'Reference project documentation',
            'Maintain consistency with existing code',
            'Consider performance implications'
        ]
    },
    'cursor': {
        'file_patterns': [
            '**/*.{js,ts,jsx,tsx}: React/TypeScript files',
            '**/*.py: Python files',
            '**/*.css: Stylesheets',
            '**/README.md: Project documentation'
        ],
        'behavior_rules': [
            'Provide inline suggestions',
            'Auto-complete based on context',
            'Suggest refactoring opportunities',
            'Highlight potential issues'
        ],
        'context_rules': [
            'Use project-specific patterns',
            'Maintain code style consistency',
            'Consider file relationships'
        ]
    },
    'windsurf': {
        'file_patterns': [
            'src/**/*.{js,ts,jsx,tsx}: Source code',
            'docs/**/*.md: Documentation',
            'config/**/*.json: Configuration',
            'tests/**/*.test.{js,ts}: Test files'
        ],
        'behavior_rules': [
            'Focus on code quality',
            'Provide architectural guidance',
            'Suggest best practices',
            'Optimize for maintainability'
        ],
        'context_rules': [
            'Consider entire project structure',
            'Maintain architectural consistency',
            'Follow established patterns'
        ]
    }
}
```

#### 3.2 Dynamic Rule Generation

```python
class RulesEngine:
    def generate_rules(self, context_analysis, target_tool):
        """
        Generate specific rules for target AI tool based on context
        """
        base_rules = RULE_TEMPLATES[target_tool]
        
        # Customize based on project context
        customized_rules = self.customize_rules(base_rules, context_analysis)
        
        # Generate file-specific rules
        file_rules = self.generate_file_rules(context_analysis, target_tool)
        
        return {
            'tool': target_tool,
            'task': context_analysis.primary_task,
            'config_file': f"{target_tool.upper()}.md",
            'rules': customized_rules,
            'file_rules': file_rules
        }
```

## 🛠️ Technical Implementation

### 1. Core Technology Stack

```python
# requirements.txt
langchain==0.1.0
langgraph==0.0.45
langfuse==2.0.0
pydantic-ai==0.0.8
graphiti==0.1.0
mem0==0.1.0
neo4j==5.15.0
qdrant-client==1.7.0
a2a==0.1.0
```

### 2. Database Configuration

```python
# config/database.py
DATABASE_CONFIG = {
    'neo4j': {
        'endpoint': 'http://localhost:7474/',
        'username': 'neo4j',
        'password': 'Mewtwo#0075'
    },
    'supabase': {
        'endpoint': 'http://localhost:8000/',
        'username': 'Mewtwo',
        'password': 'Mewtwo_Supabase#0075'
    },
    'postgres': {
        'endpoint': 'http://localhost:5437/',
        'username': 'mewtwo',
        'password': 'Mewtwo#0075'
    },
    'redis': {
        'endpoint': 'http://localhost:6380/'
    }
}
```

### 3. LLM Configuration

```python
# config/llm.py
LLM_CONFIG = {
    'primary': {
        'api_key': 'cpk_3df7be5ac77e4d9c84b6efef353f7257.a814d7d0e88b5fca8cb71ceea82354be.e9FnwMImktPQ0y5ClZ9Xa7kJiqoWYUiF',
        'model': 'Qwen/Qwen3-235B-A22B',
        'endpoint': 'https://llm.chutes.ai/v1'
    },
    'fallback': {
        'api_key': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJwYXJ0aHNoZXRoMzI2QGdtYWlsLmNvbSIsImlhdCI6MTczNjM1Njk2NH0.KXN599cevxC-QqVS439cdsOSSQX-cLiEC-ebt8Lw4oY',
        'model': 'Qwen/Qwen3-235B-A22B',
        'endpoint': 'https://api.hyperbolic.xyz/v1'
    }
}
```

## 📁 Project Structure

```
ai-context-builder/
├── backend/
│   ├── agents/
│   │   ├── context_builder.py
│   │   ├── prompt_generator.py
│   │   └── rules_engine.py
│   ├── processors/
│   │   ├── chat_importers/
│   │   ├── document_processors/
│   │   └── video_processors/
│   ├── knowledge/
│   │   ├── graph_builder.py
│   │   ├── vector_store.py
│   │   └── memory_manager.py
│   └── api/
│       ├── routes.py
│       └── websocket.py
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── hooks/
│   │   └── services/
│   └── public/
├── config/
│   ├── database.py
│   ├── llm.py
│   └── rules_templates/
├── tests/
└── docs/
```

## 🎯 Implementation Roadmap

### Phase 1: Core Infrastructure (Hours 1-2)

- [ ] Set up LangChain + LangGraph foundation
- [ ] Configure Neo4j and Qdrant connections
- [ ] Implement basic data ingestion pipeline
- [ ] Create simple frontend structure

### Phase 2: Content Processing (Hours 3-4)

- [ ] Implement document processors for all formats
- [ ] Create chat platform importers
- [ ] Build video processing pipeline
- [ ] Set up real-time processing feedback

### Phase 3: Intelligence Layer (Hours 5-6)

- [ ] Develop context analysis engine
- [ ] Implement system prompt generation
- [ ] Create rules engine for different tools
- [ ] Build knowledge graph relationships

### Phase 4: Integration & Polish (Hours 7-8)

- [ ] Connect frontend to backend
- [ ] Implement real-time updates
- [ ] Add error handling and validation
- [ ] Create output file generation

## 🔧 Usage Examples

### 1. Basic Context Building

```python
# Initialize the agent
agent = ContextBuilderAgent()

# Add various sources
agent.add_chat_history("chatgpt_export.json")
agent.add_document("project_requirements.pdf")
agent.add_video("demo_video.mp4")
agent.add_url("https://github.com/user/repo")

# Generate context
context = agent.build_context()
system_prompt = agent.generate_system_prompt(context)
```

### 2. Generate Tool-Specific Rules

```python
# Generate rules for different AI tools
rules = agent.generate_rules_for_tools([
    "gemini_cli",
    "cursor", 
    "windsurf"
])

# Output format:
# [
#   {'tool': 'gemini_cli', 'task': 'web_development', 'config_file': 'GEMINI.md'},
#   {'tool': 'cursor', 'task': 'web_development', 'config_file': 'CURSOR.md'},
#   {'tool': 'windsurf', 'task': 'web_development', 'config_file': 'WINDSURF.md'}
# ]
```

### 3. Example Generated Rules

#### Cursor Rules (CURSOR.md)

```markdown
# Cursor AI Configuration

## File Patterns
- **/*.{js,ts,jsx,tsx}: React/TypeScript source files
- **/*.py: Python modules and scripts
- **/*.css: Stylesheets and design files
- **/README.md: Project documentation

## Behavior Rules
1. Always provide complete, runnable code examples
2. Include proper error handling and validation
3. Follow project-specific coding standards
4. Suggest performance optimizations when relevant

## Context Rules
- Reference existing project patterns
- Maintain consistency with current architecture
- Consider file dependencies and relationships
- Prioritize maintainable and scalable solutions
```

## 🚀 Getting Started

### 1. Environment Setup

```bash
# Clone the repository
git clone https://github.com/your-username/ai-context-builder.git
cd ai-context-builder

# Install dependencies
pip install -r requirements.txt
npm install  # for frontend

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration
```

### 2. Start Services

```bash
# Start databases
docker-compose up -d  # Neo4j, Qdrant, Redis, PostgreSQL

# Start backend
python backend/main.py

# Start frontend
npm start
```

### 3. Basic Usage

1. Open the web interface at `http://localhost:3000`
2. Upload or import your context sources
3. Wait for processing to complete
4. Review and edit the generated system prompt
5. Download the generated rules for your AI tools

## 📊 Success Metrics

- **Context Quality**: Relevance and completeness of generated prompts
- **Rule Effectiveness**: Improvement in AI tool performance
- **Processing Speed**: Time to analyze and generate configurations
- **User Satisfaction**: Ease of use and value provided

## 🔮 Future Enhancements

- **Collaborative Features**: Team-based context building
- **Auto-Learning**: Improve rules based on usage patterns
- **Integration APIs**: Direct integration with AI development tools
- **Advanced Analytics**: Context quality metrics and optimization suggestions

---

**Ready to build the future of AI context management!** 🚀

This agent will revolutionize how developers create and manage context for AI applications, making every AI interaction more intelligent and contextually aware.



# AI Context Builder Agent - Complete Project Documentation

## 🎯 Project Vision

Create an intelligent AI agent that automatically builds comprehensive context for AI applications by ingesting information from multiple sources, then generates tailored system prompts and rule configurations for various AI development environments.

### Vision Statement

Transform the way developers interact with AI by eliminating the manual effort required to provide context, ensuring every AI interaction is informed, relevant, and optimized for the specific project domain and requirements.

### Target Audience

- **AI Application Developers**: Building applications that integrate LLMs
- **Software Engineers**: Using AI coding assistants like Cursor, Windsurf, Gemini CLI
- **Product Managers**: Defining AI agent behaviors and capabilities
- **Technical Writers**: Creating documentation for AI systems
- **Data Scientists**: Building context-aware AI models

## 🔥 Core Problem Statement

AI applications often lack proper context, resulting in generic responses and suboptimal performance. Developers spend significant time manually crafting system prompts and rules for different AI tools. This agent solves that by automatically building rich context from diverse sources and generating optimized configurations.

### Current Pain Points

1. **Context Fragmentation**: Information scattered across multiple platforms and formats
2. **Manual Prompt Engineering**: Time-consuming process requiring expertise
3. **Inconsistent AI Behavior**: Different tools producing varying results
4. **Knowledge Decay**: Context becoming outdated as projects evolve
5. **Onboarding Complexity**: New team members struggling to understand AI configurations

### Solution Benefits

- **Automated Context Building**: 90% reduction in manual context creation time
- **Consistent AI Behavior**: Standardized prompts across all tools
- **Dynamic Updates**: Context evolves with project changes
- **Knowledge Preservation**: Institutional knowledge captured and maintained
- **Team Collaboration**: Shared context accessible to all team members

## 🚀 System Architecture

```mermaid
graph TB
    subgraph "Input Layer"
        A1[Chat Platforms]
        A2[Documents]
        A3[Media Files]
        A4[URLs & APIs]
        A5[Version Control]
    end
    
    subgraph "Processing Layer"
        B1[Content Extractors]
        B2[NLP Processors]
        B3[Vision Analyzers]
        B4[Audio Transcribers]
        B5[Code Analyzers]
    end
    
    subgraph "Intelligence Layer"
        C1[Context Analyzer]
        C2[Knowledge Graph]
        C3[Semantic Indexer]
        C4[Pattern Recognizer]
        C5[Domain Classifier]
    end
    
    subgraph "Generation Layer"
        D1[Prompt Generator]
        D2[Rules Engine]
        D3[Template Manager]
        D4[Validation System]
    end
    
    subgraph "Output Layer"
        E1[System Prompts]
        E2[Tool Configurations]
        E3[Documentation]
        E4[APIs & Webhooks]
    end
    
    A1 --> B1
    A2 --> B2
    A3 --> B3
    A4 --> B4
    A5 --> B5
    
    B1 --> C1
    B2 --> C2
    B3 --> C3
    B4 --> C4
    B5 --> C5
    
    C1 --> D1
    C2 --> D2
    C3 --> D3
    C4 --> D4
    C5 --> D1
    
    D1 --> E1
    D2 --> E2
    D3 --> E3
    D4 --> E4
```

### Architecture Principles

#### 1. Modular Design

Each component is independently deployable and scalable:

- **Microservices Architecture**: Separate services for different processors
- **Plugin System**: Easy addition of new content types and platforms
- **API-First Design**: All components communicate via well-defined APIs

#### 2. Event-Driven Processing

Real-time processing with event streaming:

- **Message Queues**: Redis for job queuing and task distribution
- **Event Sourcing**: Complete audit trail of all processing steps
- **Real-time Updates**: WebSocket connections for live progress updates

#### 3. Scalable Storage

Multi-tier storage strategy:

- **Hot Storage**: Redis for frequently accessed data
- **Warm Storage**: PostgreSQL for structured data and relationships
- **Cold Storage**: Neo4j for complex relationship graphs
- **Vector Storage**: Qdrant for semantic search and similarity matching

## 📋 Feature Specifications

### 1. Multi-Source Context Ingestion

#### 1.1 Conversation Import System

##### Supported Platforms

```python
CHAT_PLATFORMS = {
    'chatgpt': {
        'export_format': ['json', 'html', 'markdown'],
        'extraction_methods': {
            'api_scraping': {
                'requires_auth': True,
                'rate_limit': '100/hour',
                'supported_features': ['conversations', 'custom_instructions', 'plugins']
            },
            'browser_extension': {
                'requires_auth': False,
                'supported_browsers': ['chrome', 'firefox', 'edge'],
                'real_time': True
            }
        },
        'data_structure': {
            'conversations': 'Array of message objects',
            'metadata': 'User preferences, model settings',
            'attachments': 'Files, images, links'
        }
    },
    'claude': {
        'export_format': ['markdown', 'json'],
        'extraction_methods': {
            'browser_extension': {
                'requires_auth': True,
                'supported_browsers': ['chrome', 'firefox'],
                'real_time': True
            },
            'api_access': {
                'requires_auth': True,
                'rate_limit': '50/hour',
                'supported_features': ['conversations', 'artifacts', 'projects']
            }
        },
        'data_structure': {
            'conversations': 'Threaded message structure',
            'artifacts': 'Code snippets, documents, visualizations',
            'projects': 'Organized conversation collections'
        }
    },
    'grok': {
        'export_format': ['html', 'json'],
        'extraction_methods': {
            'web_scraping': {
                'requires_auth': True,
                'rate_limit': '30/hour',
                'anti_bot_protection': True
            },
            'x_api': {
                'requires_auth': True,
                'rate_limit': '100/hour',
                'premium_required': True
            }
        },
        'data_structure': {
            'conversations': 'Tweet-style threading',
            'context': 'Real-time web data integration',
            'media': 'Images, videos, links'
        }
    },
    'gemini': {
        'export_format': ['json', 'protobuf'],
        'extraction_methods': {
            'google_api': {
                'requires_auth': True,
                'rate_limit': '1000/day',
                'supported_features': ['conversations', 'workspaces', 'extensions']
            },
            'workspace_sync': {
                'requires_auth': True,
                'real_time': True,
                'google_workspace_integration': True
            }
        },
        'data_structure': {
            'conversations': 'Multi-modal message structure',
            'workspaces': 'Project-based organization',
            'extensions': 'Third-party integrations'
        }
    },
    'deepseek': {
        'export_format': ['text', 'json'],
        'extraction_methods': {
            'web_scraping': {
                'requires_auth': True,
                'rate_limit': '20/hour',
                'session_management': True
            },
            'api_access': {
                'requires_auth': True,
                'rate_limit': '200/hour',
                'supported_features': ['conversations', 'code_analysis']
            }
        },
        'data_structure': {
            'conversations': 'Code-focused dialogues',
            'analysis': 'Code quality metrics',
            'suggestions': 'Optimization recommendations'
        }
    },
    'openwebui': {
        'export_format': ['json', 'sqlite'],
        'extraction_methods': {
            'local_api': {
                'requires_auth': False,
                'rate_limit': 'unlimited',
                'database_access': True
            },
            'docker_integration': {
                'requires_auth': False,
                'container_access': True,
                'volume_mounting': True
            }
        },
        'data_structure': {
            'conversations': 'Local database schema',
            'models': 'Available local models',
            'settings': 'Configuration parameters'
        }
    }
}
```

##### Chat Processing Pipeline

```python
class ChatProcessor:
    def __init__(self):
        self.extractors = {
            'chatgpt': ChatGPTExtractor(),
            'claude': ClaudeExtractor(),
            'grok': GrokExtractor(),
            'gemini': GeminiExtractor(),
            'deepseek': DeepseekExtractor(),
            'openwebui': OpenWebUIExtractor()
        }
        
    async def process_chat_export(self, platform, export_data):
        """
        Process chat export from specific platform
        """
        extractor = self.extractors[platform]
        
        # Extract conversations
        conversations = await extractor.extract_conversations(export_data)
        
        # Analyze conversation patterns
        patterns = await self.analyze_conversation_patterns(conversations)
        
        # Extract knowledge and context
        knowledge = await self.extract_knowledge(conversations)
        
        # Identify user preferences and styles
        preferences = await self.identify_user_preferences(conversations)
        
        return {
            'platform': platform,
            'conversations': conversations,
            'patterns': patterns,
            'knowledge': knowledge,
            'preferences': preferences,
            'metadata': {
                'total_messages': len(conversations),
                'date_range': self.get_date_range(conversations),
                'topics': self.extract_topics(conversations)
            }
        }
```

#### 1.2 Document Processing Pipeline

##### Document Type Handlers

```python
DOCUMENT_PROCESSORS = {
    'pdf': {
        'libraries': ['PyPDF2', 'pdfplumber', 'PyMuPDF'],
        'capabilities': {
            'text_extraction': True,
            'table_extraction': True,
            'image_extraction': True,
            'metadata_extraction': True,
            'ocr_fallback': True
        },
        'processing_pipeline': [
            'extract_text',
            'extract_tables',
            'extract_images',
            'ocr_if_needed',
            'structure_analysis',
            'semantic_chunking'
        ]
    },
    'images': {
        'libraries': ['OpenCV', 'Pillow', 'Tesseract'],
        'capabilities': {
            'text_extraction': True,
            'object_detection': True,
            'scene_analysis': True,
            'diagram_understanding': True,
            'chart_data_extraction': True
        },
        'processing_pipeline': [
            'image_preprocessing',
            'text_ocr',
            'object_detection',
            'scene_analysis',
            'diagram_parsing',
            'chart_data_extraction'
        ]
    },
    'json': {
        'libraries': ['json', 'jsonschema', 'jq'],
        'capabilities': {
            'schema_inference': True,
            'data_validation': True,
            'nested_structure_analysis': True,
            'relationship_mapping': True,
            'api_schema_detection': True
        },
        'processing_pipeline': [
            'parse_json',
            'infer_schema',
            'validate_structure',
            'extract_relationships',
            'identify_patterns',
            'generate_documentation'
        ]
    },
    'csv': {
        'libraries': ['pandas', 'numpy', 'dask'],
        'capabilities': {
            'data_profiling': True,
            'statistical_analysis': True,
            'relationship_detection': True,
            'quality_assessment': True,
            'schema_inference': True
        },
        'processing_pipeline': [
            'load_data',
            'profile_columns',
            'detect_relationships',
            'assess_quality',
            'generate_statistics',
            'create_summary'
        ]
    },
    'xml': {
        'libraries': ['lxml', 'BeautifulSoup', 'xmltodict'],
        'capabilities': {
            'structure_parsing': True,
            'namespace_handling': True,
            'xpath_queries': True,
            'validation': True,
            'transformation': True
        },
        'processing_pipeline': [
            'parse_xml',
            'extract_structure',
            'handle_namespaces',
            'validate_schema',
            'extract_data',
            'convert_to_json'
        ]
    },
    'html': {
        'libraries': ['BeautifulSoup', 'lxml', 'selenium'],
        'capabilities': {
            'content_extraction': True,
            'metadata_extraction': True,
            'link_analysis': True,
            'javascript_execution': True,
            'responsive_design_analysis': True
        },
        'processing_pipeline': [
            'parse_html',
            'extract_content',
            'extract_metadata',
            'analyze_structure',
            'extract_links',
            'clean_content'
        ]
    },
    'markdown': {
        'libraries': ['markdown', 'mistune', 'commonmark'],
        'capabilities': {
            'structure_parsing': True,
            'code_block_extraction': True,
            'link_extraction': True,
            'table_parsing': True,
            'front_matter_parsing': True
        },
        'processing_pipeline': [
            'parse_markdown',
            'extract_structure',
            'extract_code_blocks',
            'extract_links',
            'parse_tables',
            'extract_front_matter'
        ]
    },
    'url': {
        'libraries': ['requests', 'scrapy', 'playwright'],
        'capabilities': {
            'web_scraping': True,
            'javascript_rendering': True,
            'api_detection': True,
            'sitemap_analysis': True,
            'robots_txt_parsing': True
        },
        'processing_pipeline': [
            'fetch_content',
            'render_javascript',
            'extract_content',
            'analyze_structure',
            'extract_metadata',
            'follow_links'
        ]
    },
    'google_drive': {
        'libraries': ['google-api-python-client', 'google-auth'],
        'capabilities': {
            'file_discovery': True,
            'permission_checking': True,
            'version_history': True,
            'collaborative_features': True,
            'real_time_sync': True
        },
        'processing_pipeline': [
            'authenticate',
            'discover_files',
            'check_permissions',
            'download_files',
            'process_content',
            'sync_changes'
        ]
    }
}
```

##### Advanced Document Processing

```python
class DocumentProcessor:
    def __init__(self):
        self.processors = self._initialize_processors()
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
        self.chunker = SemanticChunker()
        
    async def process_document(self, file_path, document_type):
        """
        Process document with advanced analysis
        """
        processor = self.processors[document_type]
        
        # Extract content
        content = await processor.extract_content(file_path)
        
        # Analyze structure
        structure = await self.analyze_document_structure(content)
        
        # Extract entities and relationships
        entities = await self.extract_entities(content)
        relationships = await self.extract_relationships(content)
        
        # Generate semantic chunks
        chunks = await self.chunker.chunk_document(content)
        
        # Create embeddings
        embeddings = await self.create_embeddings(chunks)
        
        # Generate summary
        summary = await self.generate_summary(content)
        
        return {
            'content': content,
            'structure': structure,
            'entities': entities,
            'relationships': relationships,
            'chunks': chunks,
            'embeddings': embeddings,
            'summary': summary,
            'metadata': {
                'file_path': file_path,
                'document_type': document_type,
                'processing_time': time.time() - start_time,
                'content_length': len(content),
                'chunk_count': len(chunks)
            }
        }
```

#### 1.3 Video Information Extraction

##### Video Processing Capabilities

```python
VIDEO_PROCESSORS = {
    'mp4': {
        'libraries': ['moviepy', 'opencv-python', 'whisper'],
        'capabilities': {
            'audio_extraction': {
                'formats': ['wav', 'mp3', 'flac'],
                'quality_levels': ['low', 'medium', 'high'],
                'noise_reduction': True
            },
            'frame_analysis': {
                'keyframe_detection': True,
                'scene_segmentation': True,
                'object_tracking': True,
                'text_recognition': True
            },
            'subtitle_processing': {
                'formats': ['srt', 'vtt', 'ass'],
                'language_detection': True,
                'timing_synchronization': True
            }
        },
        'processing_pipeline': [
            'video_metadata_extraction',
            'audio_track_separation',
            'frame_extraction',
            'scene_detection',
            'audio_transcription',
            'subtitle_extraction',
            'content_analysis'
        ]
    },
    'mkv': {
        'libraries': ['ffmpeg-python', 'pymediainfo'],
        'capabilities': {
            'container_analysis': True,
            'multiple_audio_tracks': True,
            'subtitle_tracks': True,
            'chapter_extraction': True,
            'metadata_preservation': True
        },
        'processing_pipeline': [
            'container_analysis',
            'track_identification',
            'audio_processing',
            'subtitle_extraction',
            'chapter_processing',
            'metadata_extraction'
        ]
    },
    'youtube': {
        'libraries': ['yt-dlp', 'youtube-transcript-api'],
        'capabilities': {
            'video_download': {
                'quality_options': ['144p', '240p', '360p', '480p', '720p', '1080p'],
                'format_selection': True,
                'audio_only': True
            },
            'transcript_extraction': {
                'auto_generated': True,
                'manual_captions': True,
                'multiple_languages': True,
                'timestamp_preservation': True
            },
            'metadata_extraction': {
                'video_info': True,
                'comments': True,
                'related_videos': True,
                'channel_info': True
            }
        },
        'processing_pipeline': [
            'video_info_extraction',
            'transcript_download',
            'audio_extraction',
            'thumbnail_analysis',
            'comment_analysis',
            'content_categorization'
        ]
    }
}
```

##### Video Processing Implementation

```python
class VideoProcessor:
    def __init__(self):
        self.whisper_model = whisper.load_model("base")
        self.vision_model = VisionTransformer()
        self.scene_detector = SceneDetector()
        
    async def process_video(self, video_path, video_type):
        """
        Comprehensive video processing
        """
        processor = self.processors[video_type]
        
        # Extract basic metadata
        metadata = await self.extract_video_metadata(video_path)
        
        # Audio processing
        audio_path = await self.extract_audio(video_path)
        transcript = await self.transcribe_audio(audio_path)
        
        # Visual processing
        keyframes = await self.extract_keyframes(video_path)
        scenes = await self.detect_scenes(video_path)
        
        # Content analysis
        visual_content = await self.analyze_visual_content(keyframes)
        audio_content = await self.analyze_audio_content(transcript)
        
        # Generate summary
        summary = await self.generate_video_summary(
            transcript, visual_content, metadata
        )
        
        return {
            'metadata': metadata,
            'transcript': transcript,
            'scenes': scenes,
            'visual_content': visual_content,
            'audio_content': audio_content,
            'summary': summary,
            'keyframes': keyframes,
            'processing_info': {
                'video_type': video_type,
                'duration': metadata['duration'],
                'resolution': metadata['resolution'],
                'processing_time': time.time() - start_time
            }
        }
```

### 2. Intelligent System Prompt Generation

#### 2.1 Context Analysis Engine

##### Domain Classification System

```python
class DomainClassifier:
    def __init__(self):
        self.domains = {
            'web_development': {
                'keywords': ['react', 'vue', 'angular', 'javascript', 'typescript', 'html', 'css'],
                'file_patterns': ['*.js', '*.ts', '*.jsx', '*.tsx', '*.html', '*.css'],
                'frameworks': ['express', 'next.js', 'nuxt.js', 'svelte'],
                'tools': ['webpack', 'vite', 'babel', 'eslint']
            },
            'mobile_development': {
                'keywords': ['react-native', 'flutter', 'swift', 'kotlin', 'android', 'ios'],
                'file_patterns': ['*.dart', '*.swift', '*.kt', '*.java'],
                'frameworks': ['expo', 'xamarin', 'ionic'],
                'tools': ['xcode', 'android-studio', 'fastlane']
            },
            'data_science': {
                'keywords': ['python', 'pandas', 'numpy', 'scikit-learn', 'tensorflow', 'pytorch'],
                'file_patterns': ['*.py', '*.ipynb', '*.r'],
                'frameworks': ['jupyter', 'anaconda', 'mlflow'],
                'tools': ['docker', 'kubernetes', 'airflow']
            },
            'backend_development': {
                'keywords': ['api', 'database', 'server', 'microservices', 'docker'],
                'file_patterns': ['*.py', '*.js', '*.go', '*.rs', '*.java'],
                'frameworks': ['django', 'flask', 'express', 'spring'],
                'tools': ['postgresql', 'redis', 'mongodb', 'elasticsearch']
            },
            'devops': {
                'keywords': ['kubernetes', 'docker', 'ci/cd', 'terraform', 'ansible'],
                'file_patterns': ['*.yml', '*.yaml', '*.tf', '*.sh'],
                'frameworks': ['helm', 'prometheus', 'grafana'],
                'tools': ['jenkins', 'github-actions', 'gitlab-ci']
            },
            'machine_learning': {
                'keywords': ['ml', 'ai', 'neural', 'model', 'training', 'inference'],
                'file_patterns': ['*.py', '*.ipynb', '*.pkl', '*.h5'],
                'frameworks': ['tensorflow', 'pytorch', 'scikit-learn', 'transformers'],
                'tools': ['wandb', 'mlflow', 'tensorboard']
            }
        }
        
    def classify_domain(self, content):
        """
        Classify content into appropriate domain
        """
        scores = {}
        
        for domain, config in self.domains.items():
            score = 0
            
            # Keyword matching
            for keyword in config['keywords']:
                score += content.lower().count(keyword.lower())
            
            # File pattern matching
            for pattern in config['file_patterns']:
                if self._matches_pattern(content, pattern):
                    score += 5
            
            # Framework detection
            for framework in config['frameworks']:
                if framework.lower() in content.lower():
                    score += 3
            
            # Tool detection
            for tool in config['tools']:
                if tool.lower() in content.lower():
                    score += 2
            
            scores[domain] = score
        
        # Return top domain or mixed if multiple high scores
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        
        if sorted_scores[0][1] > sorted_scores[1][1] * 2:
            return sorted_scores[0][0]
        else:
            return 'mixed'
```

##### Intent Analysis System

```python
class IntentAnalyzer:
    def __init__(self):
        self.intent_patterns = {
            'code_generation': {
                'patterns': [
                    'create', 'generate', 'build', 'implement',
                    'write code', 'develop', 'make'
                ],
                'confidence_boosters': [
                    'function', 'class', 'component', 'module',
                    'algorithm', 'script'
                ]
            },
            'debugging': {
                'patterns': [
                    'fix', 'debug', 'error', 'bug', 'issue',
                    'not working', 'problem', 'troubleshoot'
                ],
                'confidence_boosters': [
                    'exception', 'traceback', 'stack trace',
                    'error message', 'failing test'
                ]
            },
            'code_review': {
                'patterns': [
                    'review', 'improve', 'optimize', 'refactor',
                    'best practices', 'code quality'
                ],
                'confidence_boosters': [
                    'performance', 'maintainability', 'readability',
                    'security', 'efficiency'
                ]
            },
            'learning': {
                'patterns': [
                    'learn', 'understand', 'explain', 'tutorial',
                    'how to', 'what is', 'why'
                ],
                'confidence_boosters': [
                    'beginner', 'guide', 'introduction',
                    'basics', 'fundamentals'
                ]
            },
            'documentation': {
                'patterns': [
                    'document', 'readme', 'guide', 'manual',
                    'documentation', 'wiki'
                ],
                'confidence_boosters': [
                    'api docs', 'user guide', 'installation',
                    'getting started', 'reference'
                ]
            }
        }
        
    def analyze_intent(self, content):
        """
        Analyze user intent from content
        """
        intent_scores = {}
        
        for intent, config in self.intent_patterns.items():
            score = 0
            
            # Pattern matching
            for pattern in config['patterns']:
                if pattern.lower() in content.lower():
                    score += 1
            
            # Confidence boosters
            for booster in config['confidence_boosters']:
                if booster.lower() in content.lower():
                    score += 0.5
            
            intent_scores[intent] = score
        
        # Normalize scores
        total_score = sum(intent_scores.values())
        if total_score > 0:
            intent_scores = {k: v/total_score for k, v in intent_scores.items()}
        
        return intent_scores
```

##### Complexity Assessment

```python
class ComplexityScorer:
    def __init__(self):
        self.complexity_indicators = {
            'low': {
                'keywords': ['simple', 'basic', 'quick', 'easy', 'minimal'],
                'code_patterns': ['single function', 'script', 'one-liner'],
                'file_count_threshold': 5,
                'line_count_threshold': 100
            },
            'medium': {
                'keywords': ['moderate', 'standard', 'typical', 'common'],
                'code_patterns': ['multiple functions', 'classes', 'modules'],
                'file_count_threshold': 20,
                'line_count_threshold': 1000
            },
            'high': {
                'keywords': ['complex', 'advanced', 'sophisticated', 'enterprise'],
                'code_patterns': ['architecture', 'design patterns', 'frameworks'],
                'file_count_threshold': 50,
                'line_count_threshold': 10000
            }
        }
        
    def score_complexity(self, content, metadata):
        """
        Score content complexity
        """
        scores = {level: 0 for level in self.complexity_indicators.keys()}
        
        # Keyword-based scoring
        for level, config in self.complexity_indicators.items():
            for keyword in config['keywords']:
                if keyword in content.lower():
                    scores[level] += 1
        
        # Code pattern analysis
        for level, config in self.complexity_indicators.items():
            for pattern in config['code_patterns']:
                if pattern in content.lower():
                    scores[level] += 2
        
        # File and line count analysis
        if 'file_count' in metadata:
            file_count = metadata['file_count']
            for level, config in self.complexity_indicators.items():
                if file_count <= config['file_count_threshold']:
                    scores[level] += 1
        
        if 'line_count' in metadata:
            line_count = metadata['line_count']
            for level, config in self.complexity_indicators.items():
                if line_count <= config['line_count_threshold']:
                    scores[level] += 1
        
        # Determine primary complexity level
        max_score = max(scores.values())
        if max_score == 0:
            return 'medium'  # Default
        
        return max(scores, key=scores.get)
```

#### 2.2 Dynamic Prompt Builder

##### Prompt Template System

```python
class PromptTemplateManager:
    def __init__(self):
        self.templates = {
            'web_development': {
                'base_template': """
You are an expert web developer with extensive experience in modern web technologies.
You specialize in creating responsive, accessible, and performant web applications.

Your expertise includes:
- Frontend frameworks: React, Vue.js, Angular, Svelte
- Backend technologies: Node.js, Python, PHP, Ruby
- Database systems: PostgreSQL, MongoDB, Redis
- DevOps tools: Docker, Kubernetes, CI/CD pipelines
- Testing frameworks: Jest, Cypress, Playwright

When helping with web development tasks:
1. Always consider modern best practices and web standards
2. Prioritize accessibility and performance
3. Suggest appropriate tools and libraries for the task
4. Include error handling and edge cases
5. Provide clear, well-commented code examples
6. Consider SEO implications when relevant
7. Suggest testing strategies

Context Information:
{context_summary}

Project Requirements:
{requirements}

Coding Standards:
{coding_standards}
""",
                'variations': {
                    'react_focused': """
You are a React development specialist with deep knowledge of the React ecosystem.
You excel at creating component-based architectures and modern React patterns.

Your React expertise includes:
- Modern React with Hooks and Context
- State management: Redux, Zustand, Jotai
- Routing: React Router, Next.js routing
- Styling: Styled Components, Tailwind CSS, CSS Modules
- Testing: React Testing Library, Jest
- Performance optimization: React.memo, useMemo, useCallback
- Server-side rendering: Next.js, Gatsby

When working with React projects:
1. Use functional components and hooks
2. Follow React best practices and patterns
3. Optimize for performance and maintainability
4. Consider accessibility in component design
5. Implement proper error boundaries
6. Use TypeScript when applicable
7. Follow the project's component structure

{context_summary}
""",
                    'fullstack_focused': """
You are a full-stack web developer with expertise in both frontend and backend technologies.
You understand the complete web application lifecycle and can architect scalable solutions.

Your full-stack expertise includes:
- Frontend: React, Vue.js, Angular
- Backend: Node.js, Python (Django/Flask), Java (Spring)
- Databases: PostgreSQL, MongoDB, Redis
- APIs: REST, GraphQL, WebSockets
- Cloud services: AWS, Azure, Google Cloud
- DevOps: Docker, Kubernetes, CI/CD

When working on full-stack projects:
1. Design scalable architecture patterns
2. Implement secure authentication and authorization
3. Optimize database queries and design
4. Consider caching strategies
5. Implement proper error handling across the stack
6. Design RESTful APIs with proper status codes
7. Consider microservices architecture when appropriate

{context_summary}

Database Schema:
{database_schema}

API Documentation:
{api_documentation}
""",
                    'mobile_web_focused': """
You are a mobile-first web developer specializing in progressive web apps and mobile optimization.
You understand the unique challenges of mobile web development and user experience.

Your mobile expertise includes:
- Progressive Web Apps (PWAs)
- Mobile-first responsive design
- Touch interactions and gestures
- Performance optimization for mobile
- Offline functionality with service workers
- Mobile debugging and testing
- Cross-platform considerations

When working on mobile web projects:
1. Design with mobile-first approach
2. Optimize for touch interactions
3. Minimize bundle sizes and loading times
4. Implement offline functionality where appropriate
5. Consider device capabilities and limitations
6. Test across different devices and browsers
7. Implement proper viewport and meta tags

{context_summary}
"""
                }
            },
            'data_science': {
                'base_template': """
You are a data science expert with deep knowledge of machine learning, statistical analysis, and data engineering.
You excel at extracting insights from complex datasets and building predictive models.

Your data science expertise includes:
- Programming languages: Python, R, SQL
- Machine learning frameworks: scikit-learn, TensorFlow, PyTorch
- Data manipulation: pandas, numpy, dask
- Visualization: matplotlib, seaborn, plotly, D3.js
- Statistical analysis: scipy, statsmodels
- Big data tools: Spark, Hadoop, Airflow
- Cloud platforms: AWS, Azure, Google Cloud

When working on data science projects:
1. Start with exploratory data analysis
2. Ensure data quality and handle missing values
3. Choose appropriate models for the problem type
4. Validate models with proper cross-validation
5. Interpret results and provide actionable insights
6. Consider ethical implications of your analysis
7. Document your methodology and assumptions

Context Information:
{context_summary}

Dataset Description:
{dataset_info}

Analysis Objectives:
{objectives}

Performance Metrics:
{metrics}
""",
                'variations': {
                    'ml_focused': """
You are a machine learning engineer specializing in building and deploying ML models at scale.
You understand the complete ML lifecycle from data preparation to model deployment.

Your ML expertise includes:
- Model development: scikit-learn, XGBoost, LightGBM
- Deep learning: TensorFlow, PyTorch, Keras
- Model deployment: Docker, Kubernetes, MLflow
- Model monitoring: Weights & Biases, TensorBoard
- Feature engineering and selection
- Hyperparameter tuning and optimization
- A/B testing for ML models

When working on ML projects:
1. Follow MLOps best practices
2. Implement proper model versioning
3. Set up comprehensive model monitoring
4. Consider model interpretability and explainability
5. Implement proper data validation and testing
6. Design scalable inference pipelines
7. Document model performance and limitations

{context_summary}
""",
                    'analytics_focused': """
You are a data analyst specializing in business intelligence and data visualization.
You excel at turning complex data into actionable business insights.

Your analytics expertise includes:
- SQL and database querying
- Statistical analysis and hypothesis testing
- Data visualization: Tableau, Power BI, Python/R
- Business intelligence tools
- A/B testing and experimentation
- Cohort analysis and customer segmentation
- Time series analysis and forecasting

When working on analytics projects:
1. Understand the business context and objectives
2. Design appropriate metrics and KPIs
3. Create clear and compelling visualizations
4. Perform statistical significance testing
5. Provide actionable recommendations
6. Consider data privacy and compliance
7. Validate findings with stakeholders

{context_summary}
"""
                }
            },
            'mobile_development': {
                'base_template': """
You are a mobile development expert with experience in both native and cross-platform development.
You understand mobile app architecture, performance optimization, and platform-specific guidelines.

Your mobile development expertise includes:
- Native development: iOS (Swift), Android (Kotlin/Java)
- Cross-platform: React Native, Flutter, Xamarin
- Mobile UI/UX design principles
- Performance optimization for mobile
- Device capabilities: camera, GPS, sensors
- App store guidelines and deployment
- Mobile testing strategies

When working on mobile projects:
1. Follow platform-specific design guidelines
2. Optimize for performance and battery life
3. Handle different screen sizes and orientations
4. Implement proper navigation patterns
5. Consider offline functionality
6. Test on real devices across different OS versions
7. Follow app store guidelines for deployment

Context Information:
{context_summary}

Platform Requirements:
{platform_requirements}

Design Guidelines:
{design_guidelines}
""",
                'variations': {
                    'ios_focused': """
You are an iOS development specialist with deep knowledge of the Apple ecosystem.
You excel at creating native iOS applications following Apple's design principles.

Your iOS expertise includes:
- Swift programming language
- UIKit and SwiftUI frameworks
- Core Data and CloudKit
- iOS SDK and Apple frameworks
- Xcode development environment
- App Store Connect and TestFlight
- iOS design patterns (MVC, MVVM, VIPER)

When working on iOS projects:
1. Follow Apple's Human Interface Guidelines
2. Use appropriate iOS design patterns
3. Optimize for different iPhone and iPad sizes
4. Implement proper memory management
5. Use Apple's recommended frameworks
6. Follow App Store Review Guidelines
7. Test on various iOS versions and devices

{context_summary}
""",
                    'android_focused': """
You are an Android development specialist with expertise in the Android ecosystem.
You excel at creating native Android applications following Material Design principles.

Your Android expertise includes:
- Kotlin and Java programming languages
- Android SDK and Android Studio
- Material Design components
- Room database and LiveData
- Android Architecture Components
- Google Play Console and deployment
- Android testing frameworks

When working on Android projects:
1. Follow Material Design guidelines
2. Use Android Architecture Components
3. Optimize for different screen sizes and densities
4. Implement proper lifecycle management
5. Use appropriate Android frameworks
6. Follow Google Play policies
7. Test across different Android versions

{context_summary}
"""
                }
            }
        }
    
    def get_template(self, domain, variation=None):
        """Get the appropriate template based on domain and variation"""
        if domain not in self.templates:
            return self.templates['web_development']['base_template']
        
        domain_templates = self.templates[domain]
        
        if variation and variation in domain_templates.get('variations', {}):
            return domain_templates['variations'][variation]
        
        return domain_templates['base_template']
    
    def customize_template(self, template, context_data):
        """Customize template with actual context data"""
        return template.format(**context_data)
```

##### Context-Aware Prompt Enhancement

```python
class ContextEnhancer:
    def __init__(self):
        self.enhancement_strategies = {
            'code_context': self._enhance_with_code_context,
            'conversation_context': self._enhance_with_conversation_context,
            'document_context': self._enhance_with_document_context,
            'project_context': self._enhance_with_project_context
        }
    
    def enhance_prompt(self, base_prompt, context_analysis):
        """Enhance base prompt with context-specific information"""
        enhanced_prompt = base_prompt
        
        # Apply each enhancement strategy
        for strategy_name, strategy_func in self.enhancement_strategies.items():
            if self._should_apply_strategy(strategy_name, context_analysis):
                enhanced_prompt = strategy_func(enhanced_prompt, context_analysis)
        
        return enhanced_prompt
    
    def _enhance_with_code_context(self, prompt, context_analysis):
        """Add code-specific context to the prompt"""
        code_context = context_analysis.get('code_context', {})
        
        if not code_context:
            return prompt
        
        enhancement = f"""

Code Context:
- Programming Languages: {', '.join(code_context.get('languages', []))}
- Frameworks: {', '.join(code_context.get('frameworks', []))}
- Libraries: {', '.join(code_context.get('libraries', []))}
- Code Style: {code_context.get('style', 'Standard')}
- Architecture Pattern: {code_context.get('architecture', 'Not specified')}

Recent Code Patterns:
{self._format_code_patterns(code_context.get('patterns', []))}

Common Issues Found:
{self._format_common_issues(code_context.get('issues', []))}
"""
        
        return prompt + enhancement
    
    def _enhance_with_conversation_context(self, prompt, context_analysis):
        """Add conversation-specific context to the prompt"""
        conv_context = context_analysis.get('conversation_context', {})
        
        if not conv_context:
            return prompt
        
        enhancement = f"""

Conversation Context:
- User's Skill Level: {conv_context.get('skill_level', 'Intermediate')}
- Preferred Communication Style: {conv_context.get('communication_style', 'Detailed')}
- Common Topics: {', '.join(conv_context.get('common_topics', []))}
- Recurring Challenges: {', '.join(conv_context.get('challenges', []))}

Previous Successful Approaches:
{self._format_successful_approaches(conv_context.get('successful_approaches', []))}

User Preferences:
{self._format_user_preferences(conv_context.get('preferences', {}))}
"""
        
        return prompt + enhancement
    
    def _enhance_with_document_context(self, prompt, context_analysis):
        """Add document-specific context to the prompt"""
        doc_context = context_analysis.get('document_context', {})
        
        if not doc_context:
            return prompt
        
        enhancement = f"""

Document Context:
- Project Documentation: {doc_context.get('has_documentation', False)}
- Requirements Specification: {doc_context.get('has_requirements', False)}
- API Documentation: {doc_context.get('has_api_docs', False)}
- Test Documentation: {doc_context.get('has_test_docs', False)}

Key Requirements:
{self._format_requirements(doc_context.get('requirements', []))}

Constraints and Limitations:
{self._format_constraints(doc_context.get('constraints', []))}

Success Criteria:
{self._format_success_criteria(doc_context.get('success_criteria', []))}
"""
        
        return prompt + enhancement
    
    def _enhance_with_project_context(self, prompt, context_analysis):
        """Add project-specific context to the prompt"""
        project_context = context_analysis.get('project_context', {})
        
        if not project_context:
            return prompt
        
        enhancement = f"""

Project Context:
- Project Type: {project_context.get('type', 'Not specified')}
- Target Audience: {project_context.get('audience', 'General')}
- Deployment Environment: {project_context.get('deployment', 'Not specified')}
- Performance Requirements: {project_context.get('performance', 'Standard')}
- Security Requirements: {project_context.get('security', 'Standard')}

Technology Stack:
{self._format_tech_stack(project_context.get('tech_stack', {}))}

Integration Requirements:
{self._format_integrations(project_context.get('integrations', []))}

Timeline and Milestones:
{self._format_timeline(project_context.get('timeline', {}))}
"""
        
        return prompt + enhancement
    
    def _should_apply_strategy(self, strategy_name, context_analysis):
        """Determine if a specific enhancement strategy should be applied"""
        context_keys = {
            'code_context': 'code_context',
            'conversation_context': 'conversation_context',
            'document_context': 'document_context',
            'project_context': 'project_context'
        }
        
        return context_keys[strategy_name] in context_analysis
    
    def _format_code_patterns(self, patterns):
        """Format code patterns for inclusion in prompt"""
        if not patterns:
            return "No specific patterns identified"
        
        formatted = []
        for pattern in patterns[:5]:  # Limit to top 5 patterns
            formatted.append(f"- {pattern['name']}: {pattern['description']}")
        
        return "\n".join(formatted)
    
    def _format_common_issues(self, issues):
        """Format common issues for inclusion in prompt"""
        if not issues:
            return "No common issues identified"
        
        formatted = []
        for issue in issues[:3]:  # Limit to top 3 issues
            formatted.append(f"- {issue['type']}: {issue['description']}")
        
        return "\n".join(formatted)
    
    def _format_successful_approaches(self, approaches):
        """Format successful approaches for inclusion in prompt"""
        if not approaches:
            return "No specific approaches identified"
        
        formatted = []
        for approach in approaches[:3]:
            formatted.append(f"- {approach['context']}: {approach['solution']}")
        
        return "\n".join(formatted)
    
    def _format_user_preferences(self, preferences):
        """Format user preferences for inclusion in prompt"""
        if not preferences:
            return "No specific preferences identified"
        
        formatted = []
        for key, value in preferences.items():
            formatted.append(f"- {key.replace('_', ' ').title()}: {value}")
        
        return "\n".join(formatted)
    
    def _format_requirements(self, requirements):
        """Format requirements for inclusion in prompt"""
        if not requirements:
            return "No specific requirements identified"
        
        formatted = []
        for req in requirements[:5]:
            formatted.append(f"- {req['priority']}: {req['description']}")
        
        return "\n".join(formatted)
    
    def _format_constraints(self, constraints):
        """Format constraints for inclusion in prompt"""
        if not constraints:
            return "No specific constraints identified"
        
        formatted = []
        for constraint in constraints[:3]:
            formatted.append(f"- {constraint['type']}: {constraint['description']}")
        
        return "\n".join(formatted)
    
    def _format_success_criteria(self, criteria):
        """Format success criteria for inclusion in prompt"""
        if not criteria:
            return "No specific success criteria identified"
        
        formatted = []
        for criterion in criteria[:3]:
            formatted.append(f"- {criterion['metric']}: {criterion['target']}")
        
        return "\n".join(formatted)
    
    def _format_tech_stack(self, tech_stack):
        """Format technology stack for inclusion in prompt"""
        if not tech_stack:
            return "No specific technology stack identified"
        
        formatted = []
        for category, technologies in tech_stack.items():
            if technologies:
                formatted.append(f"- {category.replace('_', ' ').title()}: {', '.join(technologies)}")
        
        return "\n".join(formatted)
    
    def _format_integrations(self, integrations):
        """Format integrations for inclusion in prompt"""
        if not integrations:
            return "No specific integrations identified"
        
        formatted = []
        for integration in integrations[:5]:
            formatted.append(f"- {integration['service']}: {integration['purpose']}")
        
        return "\n".join(formatted)
    
    def _format_timeline(self, timeline):
        """Format timeline for inclusion in prompt"""
        if not timeline:
            return "No specific timeline identified"
        
        formatted = []
        for milestone, deadline in timeline.items():
            formatted.append(f"- {milestone}: {deadline}")
        
        return "\n".join(formatted)
```

##### Prompt Optimization Engine

```python
class PromptOptimizer:
    def __init__(self):
        self.optimization_rules = {
            'length_optimization': self._optimize_length,
            'clarity_optimization': self._optimize_clarity,
            'specificity_optimization': self._optimize_specificity,
            'context_relevance': self._optimize_context_relevance,
            'tool_specific': self._optimize_for_tool
        }
    
    def optimize_prompt(self, prompt, context_analysis, target_tool=None):
        """Optimize prompt based on various factors"""
        optimized_prompt = prompt
        
        # Apply optimization rules
        for rule_name, rule_func in self.optimization_rules.items():
            optimized_prompt = rule_func(optimized_prompt, context_analysis, target_tool)
        
        # Validate the optimized prompt
        validation_result = self._validate_prompt(optimized_prompt)
        
        if not validation_result['valid']:
            # Apply fixes for validation issues
            optimized_prompt = self._fix_validation_issues(
                optimized_prompt, 
                validation_result['issues']
            )
        
        return optimized_prompt
    
    def _optimize_length(self, prompt, context_analysis, target_tool):
        """Optimize prompt length for the target tool"""
        if target_tool == 'gemini_cli':
            # Gemini CLI prefers more detailed prompts
            return self._expand_prompt_details(prompt, context_analysis)
        elif target_tool == 'cursor':
            # Cursor prefers concise but specific prompts
            return self._condense_prompt(prompt, keep_specifics=True)
        elif target_tool == 'windsurf':
            # Windsurf prefers structured, well-organized prompts
            return self._restructure_prompt(prompt)
        
        return prompt
    
    def _optimize_clarity(self, prompt, context_analysis, target_tool):
        """Improve prompt clarity and readability"""
        # Remove ambiguous language
        prompt = self._remove_ambiguity(prompt)
        
        # Add clear structure
        prompt = self._add_clear_structure(prompt)
        
        # Ensure consistent terminology
        prompt = self._standardize_terminology(prompt, context_analysis)
        
        return prompt
    
    def _optimize_specificity(self, prompt, context_analysis, target_tool):
        """Make prompt more specific based on context"""
        # Add specific examples from context
        prompt = self._add_context_examples(prompt, context_analysis)
        
        # Include specific requirements
        prompt = self._add_specific_requirements(prompt, context_analysis)
        
        # Add domain-specific details
        prompt = self._add_domain_specifics(prompt, context_analysis)
        
        return prompt
    
    def _optimize_context_relevance(self, prompt, context_analysis, target_tool):
        """Ensure prompt is relevant to the current context"""
        # Remove irrelevant information
        prompt = self._remove_irrelevant_info(prompt, context_analysis)
        
        # Prioritize relevant context
        prompt = self._prioritize_relevant_context(prompt, context_analysis)
        
        return prompt
    
    def _optimize_for_tool(self, prompt, context_analysis, target_tool):
        """Optimize prompt for specific AI development tool"""
        tool_optimizations = {
            'gemini_cli': self._optimize_for_gemini,
            'cursor': self._optimize_for_cursor,
            'windsurf': self._optimize_for_windsurf
        }
        
        if target_tool in tool_optimizations:
            return tool_optimizations[target_tool](prompt, context_analysis)
        
        return prompt
    
    def _optimize_for_gemini(self, prompt, context_analysis):
        """Optimize prompt specifically for Gemini CLI"""
        # Gemini CLI works well with structured, detailed prompts
        optimized = f"""
# Gemini CLI Optimized Prompt

## Role and Expertise
{self._extract_role_section(prompt)}

## Context and Requirements
{self._extract_context_section(prompt)}

## Specific Instructions
{self._extract_instructions_section(prompt)}

## Output Format
Please provide:
1. Clear, step-by-step solutions
2. Complete code examples with explanations
3. Alternative approaches when applicable
4. Potential issues and how to avoid them

## Additional Considerations
- Follow industry best practices
- Consider performance implications
- Include error handling
- Provide testing suggestions
"""
        
        return optimized
    
    def _optimize_for_cursor(self, prompt, context_analysis):
        """Optimize prompt specifically for Cursor IDE"""
        # Cursor works well with concise, action-oriented prompts
        optimized = f"""
You are a code assistant integrated with Cursor IDE. Your role is to provide:
- Precise code suggestions and completions
- Context-aware refactoring recommendations
- Real-time error detection and fixes
- Inline documentation and explanations

{self._extract_key_context(prompt)}

When providing assistance:
1. Focus on the immediate code context
2. Suggest improvements that maintain code quality
3. Provide explanations for complex logic
4. Offer multiple solutions when appropriate
5. Consider the broader codebase structure

Current project context:
{self._extract_project_context(prompt)}
"""
        
        return optimized
    
    def _optimize_for_windsurf(self, prompt, context_analysis):
        """Optimize prompt specifically for Windsurf"""
        # Windsurf prefers architectural and design-focused prompts
        optimized = f"""
You are an architectural advisor for software development. Your expertise includes:
- System design and architecture patterns
- Code organization and modularity
- Performance optimization strategies
- Scalability considerations
- Best practices and conventions

{self._extract_architectural_context(prompt)}

When providing guidance:
1. Consider the overall system architecture
2. Suggest patterns that improve maintainability
3. Recommend solutions that scale effectively
4. Provide architectural rationale for decisions
5. Consider long-term implications

Project architecture context:
{self._extract_architecture_context(prompt)}
"""
        
        return optimized
    
    def _validate_prompt(self, prompt):
        """Validate the optimized prompt for potential issues"""
        issues = []
        
        # Check prompt length
        if len(prompt) < 100:
            issues.append("Prompt too short - may lack necessary context")
        elif len(prompt) > 8000:
            issues.append("Prompt too long - may exceed token limits")
        
        # Check for clarity issues
        if prompt.count('?') > 10:
            issues.append("Too many questions - may confuse the AI")
        
        # Check for structure
        if not any(marker in prompt for marker in ['#', '##', '1.', '2.', '-']):
            issues.append("Lacks clear structure - may be hard to follow")
        
        # Check for specific requirements
        if 'When' not in prompt and 'How' not in prompt:
            issues.append("Missing behavioral guidelines")
        
        return {
            'valid': len(issues) == 0,
            'issues': issues
        }
    
    def _fix_validation_issues(self, prompt, issues):
        """Fix identified validation issues"""
        fixed_prompt = prompt
        
        for issue in issues:
            if "too short" in issue:
                fixed_prompt = self._expand_prompt(fixed_prompt)
            elif "too long" in issue:
                fixed_prompt = self._condense_prompt(fixed_prompt)
            elif "structure" in issue:
                fixed_prompt = self._add_structure(fixed_prompt)
            elif "behavioral guidelines" in issue:
                fixed_prompt = self._add_behavioral_guidelines(fixed_prompt)
        
        return fixed_prompt
```

### 3. Rules Engine for AI Development Tools
I'll continue from where you left off and add comprehensive details to each section:

### 3. Rules Engine for AI Development Tools

#### 3.1 Advanced Rule Configuration System

```python
class AdvancedRulesEngine:
    def __init__(self):
        self.rule_categories = {
            'behavioral_rules': BehavioralRulesManager(),
            'file_rules': FileRulesManager(),
            'context_rules': ContextRulesManager(),
            'output_rules': OutputRulesManager(),
            'error_handling_rules': ErrorHandlingRulesManager()
        }
        
        self.tool_specific_configs = {
            'gemini_cli': GeminiCliConfig(),
            'cursor': CursorConfig(),
            'windsurf': WindsurfConfig(),
            'custom_tools': CustomToolsConfig()
        }
    
    def generate_comprehensive_rules(self, context_analysis, target_tools):
        """Generate comprehensive rules for multiple AI development tools"""
        rules_output = []
        
        for tool in target_tools:
            tool_rules = self._generate_tool_specific_rules(tool, context_analysis)
            rules_output.append(tool_rules)
        
        return rules_output
    
    def _generate_tool_specific_rules(self, tool, context_analysis):
        """Generate rules specific to each AI development tool"""
        tool_config = self.tool_specific_configs.get(tool)
        if not tool_config:
            raise ValueError(f"Unsupported tool: {tool}")
        
        # Generate different categories of rules
        behavioral_rules = self._generate_behavioral_rules(tool, context_analysis)
        file_rules = self._generate_file_rules(tool, context_analysis)
        context_rules = self._generate_context_rules(tool, context_analysis)
        output_rules = self._generate_output_rules(tool, context_analysis)
        error_handling_rules = self._generate_error_handling_rules(tool, context_analysis)
        
        return {
            'tool': tool,
            'task': context_analysis.get('primary_task', 'development'),
            'config_file': f"{tool.upper().replace('_', '-')}.md",
            'rules': {
                'behavioral': behavioral_rules,
                'file_patterns': file_rules,
                'context': context_rules,
                'output': output_rules,
                'error_handling': error_handling_rules
            },
            'metadata': {
                'generated_at': datetime.now().isoformat(),
                'context_hash': self._generate_context_hash(context_analysis),
                'version': '1.0'
            }
        }
    
    def _generate_behavioral_rules(self, tool, context_analysis):
        """Generate behavioral rules for the specific tool"""
        base_rules = {
            'communication_style': self._determine_communication_style(context_analysis),
            'response_format': self._determine_response_format(tool, context_analysis),
            'interaction_patterns': self._determine_interaction_patterns(tool, context_analysis),
            'problem_solving_approach': self._determine_problem_solving_approach(context_analysis)
        }
        
        # Tool-specific behavioral customizations
        if tool == 'gemini_cli':
            base_rules.update({
                'detail_level': 'comprehensive',
                'explanation_style': 'step_by_step',
                'code_examples': 'always_include',
                'alternative_solutions': 'provide_when_relevant',
                'follow_up_questions': 'ask_clarifying_questions',
                'learning_mode': 'explain_concepts_thoroughly'
            })
        elif tool == 'cursor':
            base_rules.update({
                'detail_level': 'concise_but_complete',
                'explanation_style': 'inline_comments',
                'code_examples': 'contextual_snippets',
                'real_time_feedback': 'enabled',
                'auto_completion': 'intelligent_suggestions',
                'refactoring_hints': 'provide_when_beneficial'
            })
        elif tool == 'windsurf':
            base_rules.update({
                'detail_level': 'architectural_focus',
                'explanation_style': 'design_rationale',
                'code_examples': 'pattern_demonstrations',
                'scalability_considerations': 'always_consider',
                'performance_focus': 'highlight_optimizations',
                'maintainability': 'prioritize_long_term_health'
            })
        
        return base_rules
    
    def _generate_file_rules(self, tool, context_analysis):
        """Generate file-specific rules and patterns"""
        project_type = context_analysis.get('project_type', 'general')
        tech_stack = context_analysis.get('tech_stack', {})
        
        file_rules = {
            'patterns': self._get_file_patterns(project_type, tech_stack),
            'exclusions': self._get_file_exclusions(project_type),
            'processing_rules': self._get_processing_rules(tool, project_type),
            'organization': self._get_file_organization_rules(project_type)
        }
        
        # Tool-specific file handling
        if tool == 'cursor':
            file_rules.update({
                'auto_suggestions': {
                    '*.py': {
                        'type_hints': 'always_suggest',
                        'docstrings': 'google_style',
                        'imports': 'organize_automatically',
                        'formatting': 'black_compatible'
                    },
                    '*.js': {
                        'es6_features': 'prefer_modern_syntax',
                        'async_patterns': 'suggest_async_await',
                        'error_handling': 'try_catch_blocks',
                        'linting': 'eslint_integration'
                    },
                    '*.tsx': {
                        'component_patterns': 'functional_components',
                        'hooks': 'suggest_appropriate_hooks',
                        'props_typing': 'typescript_interfaces',
                        'state_management': 'context_or_redux'
                    },
                    '*.css': {
                        'responsive_design': 'mobile_first',
                        'naming_convention': 'bem_methodology',
                        'performance': 'optimize_selectors',
                        'accessibility': 'wcag_compliance'
                    }
                },
                'refactoring_rules': {
                    'extract_method': 'Suggest when functions exceed 20 lines',
                    'extract_component': 'Suggest when React components exceed 100 lines',
                    'optimize_imports': 'Auto-organize imports on save',
                    'dead_code_detection': 'Highlight unused variables and functions'
                }
            })
        elif tool == 'windsurf':
            file_rules.update({
                'architectural_patterns': {
                    'src/': 'Main application source code',
                    'components/': 'Reusable UI components',
                    'services/': 'Business logic and API calls',
                    'utils/': 'Helper functions and utilities',
                    'types/': 'TypeScript type definitions',
                    'hooks/': 'Custom React hooks',
                    'contexts/': 'React context providers',
                    'assets/': 'Static assets and resources'
                },
                'code_quality_rules': {
                    'complexity_threshold': 'Warn when cyclomatic complexity > 10',
                    'test_coverage': 'Maintain minimum 80% coverage',
                    'dependency_analysis': 'Monitor circular dependencies',
                    'performance_metrics': 'Track bundle size and load times'
                }
            })
        
        return file_rules
    
    def _generate_context_rules(self, tool, context_analysis):
        """Generate context-aware rules"""
        context_rules = {
            'project_awareness': self._get_project_awareness_rules(context_analysis),
            'dependency_management': self._get_dependency_rules(context_analysis),
            'integration_patterns': self._get_integration_patterns(context_analysis),
            'best_practices': self._get_best_practices_rules(context_analysis)
        }
        
        # Add tool-specific context rules
        if tool == 'windsurf':
            context_rules.update({
                'architectural_patterns': {
                    'microservices': 'Consider service boundaries and communication',
                    'monolithic': 'Focus on module separation and interfaces',
                    'jamstack': 'Optimize for static generation and CDN',
                    'serverless': 'Design for stateless execution'
                },
                'design_principles': {
                    'solid_principles': 'Apply SOLID design principles',
                    'dry_principle': 'Avoid code duplication',
                    'separation_of_concerns': 'Maintain clear responsibilities',
                    'inversion_of_control': 'Use dependency injection'
                },
                'scalability_patterns': {
                    'caching_strategies': 'Implement appropriate caching layers',
                    'load_balancing': 'Consider horizontal scaling',
                    'database_optimization': 'Optimize queries and indexes',
                    'cdn_integration': 'Leverage content delivery networks'
                }
            })
        elif tool == 'gemini_cli':
            context_rules.update({
                'learning_context': {
                    'skill_level': 'Adapt explanations to user expertise',
                    'domain_knowledge': 'Build on existing knowledge',
                    'learning_goals': 'Align with user objectives',
                    'preferred_examples': 'Use relevant, contextual examples'
                },
                'project_context': {
                    'current_state': 'Understand where the project stands',
                    'next_steps': 'Suggest logical progression',
                    'blockers': 'Identify and address obstacles',
                    'resources': 'Recommend additional learning materials'
                }
            })
        
        return context_rules
    
    def _generate_output_rules(self, tool, context_analysis):
        """Generate output formatting and presentation rules"""
        output_rules = {
            'code_formatting': self._get_code_formatting_rules(context_analysis),
            'documentation_style': self._get_documentation_style(context_analysis),
            'response_structure': self._get_response_structure(tool, context_analysis),
            'visual_presentation': self._get_visual_presentation_rules(tool)
        }
        
        # Tool-specific output customizations
        if tool == 'cursor':
            output_rules.update({
                'inline_suggestions': {
                    'completion_style': 'ghost_text',
                    'confidence_threshold': 0.7,
                    'multi_line_suggestions': 'enabled',
                    'context_aware_completions': 'use_surrounding_code'
                },
                'diff_presentation': {
                    'highlight_changes': 'semantic_highlighting',
                    'show_line_numbers': 'relative_to_cursor',
                    'merge_conflicts': 'intelligent_resolution',
                    'preview_mode': 'side_by_side'
                }
            })
        elif tool == 'windsurf':
            output_rules.update({
                'architectural_diagrams': {
                    'component_relationships': 'show_dependencies',
                    'data_flow': 'visualize_information_flow',
                    'system_boundaries': 'highlight_interfaces',
                    'deployment_view': 'show_infrastructure'
                },
                'code_analysis': {
                    'complexity_metrics': 'cyclomatic_complexity',
                    'dependency_graph': 'show_module_relationships',
                    'performance_insights': 'highlight_bottlenecks',
                    'security_analysis': 'identify_vulnerabilities'
                }
            })
        
        return output_rules
    
    def _generate_error_handling_rules(self, tool, context_analysis):
        """Generate error handling and debugging rules"""
        error_rules = {
            'error_detection': self._get_error_detection_rules(context_analysis),
            'debugging_assistance': self._get_debugging_rules(tool, context_analysis),
            'recovery_strategies': self._get_recovery_strategies(context_analysis),
            'prevention_measures': self._get_prevention_measures(context_analysis)
        }
        
        # Tool-specific error handling
        if tool == 'cursor':
            error_rules.update({
                'real_time_validation': {
                    'syntax_checking': 'highlight_immediately',
                    'type_checking': 'typescript_integration',
                    'linting': 'eslint_prettier_integration',
                    'import_resolution': 'check_module_existence'
                },
                'error_suggestions': {
                    'quick_fixes': 'provide_auto_fixes',
                    'refactoring_hints': 'suggest_improvements',
                    'documentation_links': 'link_to_relevant_docs',
                    'stack_overflow_integration': 'find_similar_issues'
                }
            })
        elif tool == 'gemini_cli':
            error_rules.update({
                'educational_debugging': {
                    'explain_error_causes': 'provide_detailed_explanations',
                    'step_by_step_resolution': 'guide_through_fixes',
                    'alternative_approaches': 'suggest_different_methods',
                    'learning_opportunities': 'turn_errors_into_lessons'
                }
            })
        
        return error_rules
```

#### 3.2 Tool-Specific Configuration Classes

```python
class GeminiCliConfig:
    """Configuration specific to Gemini CLI tool"""
    
    def __init__(self):
        self.default_settings = {
            'interaction_mode': 'conversational',
            'response_format': 'markdown',
            'code_execution': 'sandbox_mode',
            'learning_assistance': 'enabled'
        }
    
    def generate_config_file(self, rules_data):
        """Generate Gemini CLI specific configuration file"""
        config = f"""# Gemini CLI Configuration

## Core Settings
- **Interaction Mode**: {rules_data['behavioral']['communication_style']}
- **Detail Level**: {rules_data['behavioral']['detail_level']}
- **Learning Mode**: {rules_data['behavioral']['learning_mode']}

## File Processing Rules
{self._format_file_rules(rules_data['file_patterns'])}

## Context Awareness
{self._format_context_rules(rules_data['context'])}

## Output Formatting
{self._format_output_rules(rules_data['output'])}

## Error Handling
{self._format_error_rules(rules_data['error_handling'])}
"""
        return config

class CursorConfig:
    """Configuration specific to Cursor AI tool"""
    
    def __init__(self):
        self.default_settings = {
            'auto_completion': 'intelligent',
            'inline_suggestions': 'enabled',
            'refactoring_hints': 'contextual',
            'real_time_feedback': 'immediate'
        }
    
    def generate_config_file(self, rules_data):
        """Generate Cursor specific configuration file"""
        config = f"""# Cursor AI Configuration

## Editor Integration
- **Auto Completion**: {rules_data['behavioral']['auto_completion']}
- **Inline Suggestions**: {rules_data['output']['inline_suggestions']}
- **Real-time Feedback**: {rules_data['behavioral']['real_time_feedback']}

## Code Quality
{self._format_code_quality_rules(rules_data)}

## File Patterns and Processing
{self._format_file_patterns(rules_data['file_patterns'])}

## Refactoring Rules
{self._format_refactoring_rules(rules_data)}

## Error Detection and Correction
{self._format_error_detection(rules_data['error_handling'])}
"""
        return config

class WindsurfConfig:
    """Configuration specific to Windsurf AI tool"""
    
    def __init__(self):
        self.default_settings = {
            'architectural_focus': 'system_design',
            'scalability_analysis': 'enabled',
            'performance_optimization': 'proactive',
            'maintainability_checks': 'continuous'
        }
    
    def generate_config_file(self, rules_data):
        """Generate Windsurf specific configuration file"""
        config = f"""# Windsurf AI Configuration

## Architectural Focus
- **Design Approach**: {rules_data['behavioral']['architectural_focus']}
- **Scalability**: {rules_data['behavioral']['scalability_considerations']}
- **Performance**: {rules_data['behavioral']['performance_focus']}

## System Design Patterns
{self._format_architectural_patterns(rules_data['context'])}

## Code Quality Metrics
{self._format_quality_metrics(rules_data)}

## Project Structure
{self._format_project_structure(rules_data['file_patterns'])}

## Performance Monitoring
{self._format_performance_rules(rules_data)}
"""
        return config
```

#### 3.3 Dynamic Rule Adaptation System

```python
class DynamicRuleAdapter:
    """Adapts rules based on real-time context and user feedback"""
    
    def __init__(self):
        self.feedback_analyzer = FeedbackAnalyzer()
        self.context_monitor = ContextMonitor()
        self.rule_optimizer = RuleOptimizer()
    
    def adapt_rules(self, current_rules, user_feedback, context_changes):
        """Dynamically adapt rules based on feedback and context changes"""
        
        # Analyze user feedback patterns
        feedback_insights = self.feedback_analyzer.analyze(user_feedback)
        
        # Monitor context changes
        context_drift = self.context_monitor.detect_drift(context_changes)
        
        # Optimize rules based on insights
        optimized_rules = self.rule_optimizer.optimize(
            current_rules, 
            feedback_insights, 
            context_drift
        )
        
        return optimized_rules
    
    def learn_from_interactions(self, interaction_history):
        """Learn from user interactions to improve rule generation"""
        patterns = self._extract_usage_patterns(interaction_history)
        preferences = self._identify_user_preferences(interaction_history)
        
        # Update rule templates based on learning
        self._update_rule_templates(patterns, preferences)
        
        return {
            'patterns_learned': patterns,
            'preferences_identified': preferences,
            'templates_updated': True
        }

class RuleValidator:
    """Validates generated rules for consistency and effectiveness"""
    
    def validate_rules(self, rules_set):
        """Validate rules for consistency, completeness, and effectiveness"""
        validation_results = {
            'consistency_check': self._check_consistency(rules_set),
            'completeness_check': self._check_completeness(rules_set),
            'effectiveness_check': self._check_effectiveness(rules_set),
            'conflict_detection': self._detect_conflicts(rules_set)
        }
        
        return validation_results
    
    def _check_consistency(self, rules_set):
        """Check for consistency across different rule categories"""
        consistency_issues = []
        
        # Check behavioral vs output rule alignment
        if rules_set['behavioral']['detail_level'] == 'concise' and \
           rules_set['output']['response_structure'] == 'comprehensive':
            consistency_issues.append("Behavioral and output rules conflict")
        
        # Check file rules vs context rules alignment
        # ... additional consistency checks
        
        return consistency_issues
    
    def _check_completeness(self, rules_set):
        """Check if all necessary rule categories are present"""
        required_categories = [
            'behavioral', 'file_patterns', 'context', 
            'output', 'error_handling'
        ]
        
        missing_categories = [
            category for category in required_categories 
            if category not in rules_set
        ]
        
        return missing_categories
    
    def _check_effectiveness(self, rules_set):
        """Check if rules are likely to be effective"""
        effectiveness_score = 0
        
        # Score based on rule specificity
        if 'specific_examples' in str(rules_set):
            effectiveness_score += 20
        
        # Score based on context awareness
        if 'project_awareness' in rules_set.get('context', {}):
            effectiveness_score += 25
        
        # Score based on tool-specific optimizations
        if 'tool_specific' in str(rules_set):
            effectiveness_score += 30
        
        return effectiveness_score
```

#### 3.4 Rule Templates and Examples

```python
COMPREHENSIVE_RULE_TEMPLATES = {
    'web_development': {
        'gemini_cli': {
            'behavioral': {
                'communication_style': 'tutorial_based',
                'explanation_depth': 'comprehensive_with_examples',
                'code_examples': 'full_working_examples',
                'best_practices': 'always_include'
            },
            'file_patterns': {
                'frontend': ['**/*.{js,jsx,ts,tsx,vue,svelte}'],
                'backend': ['**/*.{py,js,php,rb,go,rs}'],
                'styles': ['**/*.{css,scss,sass,less}'],
                'config': ['**/*.{json,yaml,yml,toml}'],
                'tests': ['**/*.{test,spec}.{js,ts,py}']
            },
            'context_rules': {
                'framework_awareness': 'detect_and_adapt_to_framework',
                'dependency_management': 'suggest_compatible_packages',
                'security_considerations': 'highlight_vulnerabilities',
                'performance_optimization': 'suggest_improvements'
            }
        },
        'cursor': {
            'behavioral': {
                'auto_completion': 'context_aware_intelligent',
                'refactoring_suggestions': 'proactive_optimization',
                'error_detection': 'real_time_validation',
                'code_quality': 'continuous_improvement'
            },
            'file_patterns': {
                'javascript': {
                    'patterns': ['**/*.{js,jsx,ts,tsx}'],
                    'suggestions': {
                        'import_organization': 'auto_sort_imports',
                        'code_formatting': 'prettier_integration',
                        'linting': 'eslint_airbnb_config',
                        'type_checking': 'typescript_strict_mode'
                    }
                },
                'python': {
                    'patterns': ['**/*.py'],
                    'suggestions': {
                        'code_formatting': 'black_formatter',
                        'import_sorting': 'isort_integration',
                        'type_hints': 'mypy_compatibility',
                        'documentation': 'google_docstring_style'
                    }
                }
            }
        },
        'windsurf': {
            'behavioral': {
                'architectural_focus': 'scalable_maintainable_systems',
                'design_patterns': 'suggest_appropriate_patterns',
                'performance_analysis': 'identify_bottlenecks',
                'security_review': 'continuous_security_assessment'
            },
            'architectural_patterns': {
                'frontend_architecture': {
                    'component_structure': 'atomic_design_methodology',
                    'state_management': 'redux_toolkit_or_zustand',
                    'routing': 'react_router_with_code_splitting',
                    'styling': 'styled_components_or_tailwind'
                },
                'backend_architecture': {
                    'api_design': 'restful_or_graphql',
                    'database_design': 'normalized_with_indexes',
                    'caching_strategy': 'redis_or_memcached',
                    'authentication': 'jwt_with_refresh_tokens'
                }
            }
        }
    },
    'data_science': {
        'gemini_cli': {
            'behavioral': {
                'explanation_style': 'mathematical_concepts_explained',
                'code_examples': 'jupyter_notebook_style',
                'data_visualization': 'always_include_plots',
                'statistical_context': 'explain_statistical_significance'
            },
            'file_patterns': {
                'notebooks': ['**/*.ipynb'],
                'scripts': ['**/*.py'],
                'data': ['**/*.{csv,json,parquet,hdf5}'],
                'models': ['**/*.{pkl,joblib,h5,pb}']
            },
            'context_rules': {
                'data_preprocessing': 'suggest_cleaning_strategies',
                'model_selection': 'compare_multiple_algorithms',
                'evaluation_metrics': 'appropriate_for_problem_type',
                'visualization_best_practices': 'clear_informative_plots'
            }
        },
        'cursor': {
            'behavioral': {
                'auto_completion': 'pandas_numpy_sklearn_aware',
                'data_exploration': 'suggest_eda_techniques',
                'model_debugging': 'identify_common_issues',
                'performance_optimization': 'vectorization_suggestions'
            },
            'file_patterns': {
                'python_data': {
                    'patterns': ['**/*.py'],
                    'suggestions': {
                        'imports': 'standard_data_science_imports',
                        'data_loading': 'efficient_io_operations',
                        'error_handling': 'robust_data_validation',
                        'memory_management': 'optimize_dataframe_operations'
                    }
                }
            }
        }
    },
    'mobile_development': {
        'react_native': {
            'gemini_cli': {
                'behavioral': {
                    'platform_considerations': 'ios_android_differences',
                    'performance_focus': 'mobile_optimization',
                    'ui_ux_guidance': 'mobile_design_patterns',
                    'testing_approach': 'device_specific_testing'
                },
                'file_patterns': {
                    'components': ['**/*.{tsx,jsx}'],
                    'screens': ['**/screens/**/*.{tsx,jsx}'],
                    'navigation': ['**/navigation/**/*.{tsx,jsx}'],
                    'assets': ['**/assets/**/*.{png,jpg,svg}']
                }
            }
        },
        'flutter': {
            'gemini_cli': {
                'behavioral': {
                    'widget_composition': 'explain_widget_tree',
                    'state_management': 'riverpod_or_bloc_patterns',
                    'performance_tips': 'widget_optimization',
                    'platform_integration': 'native_features_usage'
                },
                'file_patterns': {
                    'dart_files': ['**/*.dart'],
                    'assets': ['**/assets/**/*'],
                    'config': ['pubspec.yaml', 'analysis_options.yaml']
                }
            }
        }
    }
}
```

#### 3.5 Rule Output Generation

```python
class RuleOutputGenerator:
    """Generates formatted output files for different AI tools"""
    
    def __init__(self):
        self.template_engine = TemplateEngine()
        self.file_formatter = FileFormatter()
    
    def generate_all_outputs(self, rules_data):
        """Generate all output files for the configured tools"""
        outputs = {}
        
        for tool_config in rules_data:
            tool_name = tool_config['tool']
            output_file = self._generate_tool_output(tool_config)
            outputs[tool_name] = {
                'filename': tool_config['config_file'],
                'content': output_file,
                'metadata': tool_config['metadata']
            }
        
        return outputs
    
    def _generate_tool_output(self, tool_config):
        """Generate formatted output for a specific tool"""
        tool_name = tool_config['tool']
        
        if tool_name == 'gemini_cli':
            return self._generate_gemini_output(tool_config)
        elif tool_name == 'cursor':
            return self._generate_cursor_output(tool_config)
        elif tool_name == 'windsurf':
            return self._generate_windsurf_output(tool_config)
        else:
            return self._generate_generic_output(tool_config)
    
    def _generate_gemini_output(self, tool_config):
        """Generate Gemini CLI specific output"""
        rules = tool_config['rules']
        
        output = f"""# Gemini CLI Configuration
*Generated on {tool_config['metadata']['generated_at']}*

## 🎯 Primary Task
{tool_config['task'].replace('_', ' ').title()}

## 🤖 Behavioral Configuration

### Communication Style
- **Approach**: {rules['behavioral']['communication_style']}
- **Detail Level**: {rules['behavioral']['detail_level']}
- **Explanation Style**: {rules['behavioral']['explanation_style']}
- **Learning Mode**: {rules['behavioral']['learning_mode']}

### Response Patterns
- **Code Examples**: {rules['behavioral']['code_examples']}
- **Alternative Solutions**: {rules['behavioral']['alternative_solutions']}
- **Follow-up Questions**: {rules['behavioral']['follow_up_questions']}

## 📁 File Processing Rules

### Supported Patterns
{self._format_file_patterns(rules['file_patterns'])}

### Processing Guidelines
{self._format_processing_guidelines(rules['file_patterns'])}

## 🧠 Context Awareness

### Project Understanding
{self._format_project_awareness(rules['context'])}

### Learning Context
{self._format_learning_context(rules['context'])}

## 📝 Output Formatting

### Code Presentation
{self._format_code_presentation(rules['output'])}

### Documentation Style
{self._format_documentation_style(rules['output'])}

## 🚨 Error Handling

### Educational Debugging
{self._format_educational_debugging(rules['error_handling'])}

### Recovery Strategies
{self._format_recovery_strategies(rules['error_handling'])}

---
*This configuration is optimized for your specific project context and will help Gemini CLI provide more relevant and targeted assistance.*
"""
        return output
    
    def _generate_cursor_output(self, tool_config):
        """Generate Cursor specific output"""
        rules = tool_config['rules']
        
        output = f"""# Cursor AI Configuration
*Generated on {tool_config['metadata']['generated_at']}*

## 🎯 Primary Task
{tool_config['task'].replace('_', ' ').title()}

## ⚡ Editor Integration

### Auto-Completion Settings
- **Style**: {rules['behavioral']['auto_completion']}
- **Confidence Threshold**: {rules['output']['inline_suggestions']['confidence_threshold']}
- **Multi-line Suggestions**: {rules['output']['inline_suggestions']['multi_line_suggestions']}

### Real-time Feedback
- **Validation**: {rules['error_handling']['real_time_validation']}
- **Refactoring Hints**: {rules['behavioral']['refactoring_hints']}

## 📁 File-Specific Rules

{self._format_cursor_file_rules(rules['file_patterns'])}

## 🔧 Refactoring Configuration

{self._format_refactoring_rules(rules['file_patterns'])}

## 🐛 Error Detection & Correction

### Real-time Validation
{self._format_real_time_validation(rules['error_handling'])}

### Quick Fixes
{self._format_quick_fixes(rules['error_handling'])}

## 🎨 Code Quality

### Formatting Rules
{self._format_code_quality_rules(rules)}

---
*This configuration optimizes Cursor's AI assistance for your specific development workflow.*
"""
        return output
    
    def _generate_windsurf_output(self, tool_config):
        """Generate Windsurf specific output"""
        rules = tool_config['rules']
        
        output = f"""# Windsurf AI Configuration
*Generated on {tool_config['metadata']['generated_at']}*

## 🎯 Primary Task
{tool_config['task'].replace('_', ' ').title()}

## 🏗️ Architectural Focus

### Design Approach
- **Primary Focus**: {rules['behavioral']['architectural_focus']}
- **Scalability**: {rules['behavioral']['scalability_considerations']}
- **Performance**: {rules['behavioral']['performance_focus']}
- **Maintainability**: {rules['behavioral']['maintainability']}

## 🎨 Design Patterns

### Architectural Patterns
{self._format_architectural_patterns(rules['context
```