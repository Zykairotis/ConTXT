"""
Code file processor.

This module provides a processor for source code files that extracts structure,
functions, classes, and other code elements with language-specific handling.
"""
import logging
import re
from typing import Dict, Any, List, Optional, Tuple, Set
from pathlib import Path

# Code parsing libraries
try:
    import pygments
    from pygments.lexers import get_lexer_for_filename, get_lexer_by_name
    from pygments.token import Token
    PYGMENTS_AVAILABLE = True
except ImportError:
    PYGMENTS_AVAILABLE = False

from app.processors.base import BaseProcessor

logger = logging.getLogger(__name__)

class CodeProcessor(BaseProcessor):
    """
    Processor for source code files.
    
    This processor extracts structure, functions, classes, and other code elements
    from source code files with language-specific handling.
    """
    
    # Language-specific patterns for extracting structure
    LANGUAGE_PATTERNS = {
        'python': {
            'function': r'def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(',
            'class': r'class\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*(\(|:)',
            'import': r'(?:from\s+([a-zA-Z0-9_.]+)\s+)?import\s+([a-zA-Z0-9_.*]+)',
            'comment': r'#.*$',
            'docstring': r'"""[\s\S]*?"""|\'\'\'[\s\S]*?\'\'\'',
        },
        'javascript': {
            'function': r'(?:function\s+([a-zA-Z_][a-zA-Z0-9_]*)|(?:const|let|var)\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*(?:async\s*)?(?:function|\([^)]*\)\s*=>))',
            'class': r'class\s+([a-zA-Z_][a-zA-Z0-9_]*)',
            'import': r'import\s+(?:\*\s+as\s+([a-zA-Z0-9_]+)|{([^}]+)}|([a-zA-Z0-9_]+))\s+from\s+[\'"]([^\'"]+)[\'"]',
            'comment': r'//.*$|/\*[\s\S]*?\*/',
        },
        'typescript': {
            'function': r'(?:function\s+([a-zA-Z_][a-zA-Z0-9_]*)|(?:const|let|var)\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*(?:async\s*)?(?:function|\([^)]*\)\s*=>))',
            'class': r'class\s+([a-zA-Z_][a-zA-Z0-9_]*)',
            'interface': r'interface\s+([a-zA-Z_][a-zA-Z0-9_]*)',
            'type': r'type\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*=',
            'import': r'import\s+(?:\*\s+as\s+([a-zA-Z0-9_]+)|{([^}]+)}|([a-zA-Z0-9_]+))\s+from\s+[\'"]([^\'"]+)[\'"]',
            'comment': r'//.*$|/\*[\s\S]*?\*/',
        },
        'java': {
            'function': r'(?:public|private|protected|static|\s) +[\w\<\>\[\]]+\s+(\w+) *\([^\)]*\)',
            'class': r'(?:public|private|protected|static|\s) +class +(\w+)',
            'interface': r'(?:public|private|protected|static|\s) +interface +(\w+)',
            'import': r'import\s+([a-zA-Z0-9_.]+(?:\.[*])?);',
            'comment': r'//.*$|/\*[\s\S]*?\*/',
        },
        'c': {
            'function': r'(?:[a-zA-Z_][a-zA-Z0-9_]*\s+)+([a-zA-Z_][a-zA-Z0-9_]*)\s*\([^;]*\)\s*{',
            'struct': r'struct\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*{',
            'include': r'#include\s+[<"]([^>"]+)[>"]',
            'comment': r'//.*$|/\*[\s\S]*?\*/',
        },
        'cpp': {
            'function': r'(?:[a-zA-Z_][a-zA-Z0-9_:]*\s+)+([a-zA-Z_][a-zA-Z0-9_]*)\s*\([^;]*\)\s*{',
            'class': r'class\s+([a-zA-Z_][a-zA-Z0-9_]*)',
            'struct': r'struct\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*{',
            'include': r'#include\s+[<"]([^>"]+)[>"]',
            'namespace': r'namespace\s+([a-zA-Z_][a-zA-Z0-9_]*)',
            'comment': r'//.*$|/\*[\s\S]*?\*/',
        },
        'go': {
            'function': r'func\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(',
            'struct': r'type\s+([a-zA-Z_][a-zA-Z0-9_]*)\s+struct',
            'interface': r'type\s+([a-zA-Z_][a-zA-Z0-9_]*)\s+interface',
            'import': r'import\s+(?:"([^"]+)"|(?:\(\s*(?:"[^"]+"\s*)+\)))',
            'comment': r'//.*$|/\*[\s\S]*?\*/',
        },
        'rust': {
            'function': r'fn\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(',
            'struct': r'struct\s+([a-zA-Z_][a-zA-Z0-9_]*)',
            'enum': r'enum\s+([a-zA-Z_][a-zA-Z0-9_]*)',
            'trait': r'trait\s+([a-zA-Z_][a-zA-Z0-9_]*)',
            'impl': r'impl(?:\s+<[^>]+>)?\s+(?:[^{]+)\s+for\s+([a-zA-Z_][a-zA-Z0-9_]*)',
            'use': r'use\s+([^;]+);',
            'comment': r'//.*$|/\*[\s\S]*?\*/',
        },
        # Add more languages as needed
    }
    
    # File extension to language mapping
    EXTENSION_TO_LANGUAGE = {
        '.py': 'python',
        '.js': 'javascript',
        '.ts': 'typescript',
        '.jsx': 'javascript',
        '.tsx': 'typescript',
        '.java': 'java',
        '.c': 'c',
        '.h': 'c',
        '.cpp': 'cpp',
        '.hpp': 'cpp',
        '.cc': 'cpp',
        '.go': 'go',
        '.rs': 'rust',
        # Add more extensions as needed
    }
    
    def __init__(self, 
                 extract_structure: bool = True,
                 extract_dependencies: bool = True,
                 extract_comments: bool = True,
                 highlight_syntax: bool = True,
                 **kwargs):
        """
        Initialize the code processor.
        
        Args:
            extract_structure: Whether to extract code structure (functions, classes, etc.)
            extract_dependencies: Whether to extract dependencies (imports, includes, etc.)
            extract_comments: Whether to extract comments and docstrings
            highlight_syntax: Whether to perform syntax highlighting
            **kwargs: Additional options for the base processor
        """
        super().__init__(**kwargs)
        
        if highlight_syntax and not PYGMENTS_AVAILABLE:
            logger.warning(
                "Pygments is required for syntax highlighting. "
                "Install it with: pip install pygments"
            )
            highlight_syntax = False
        
        self.extract_structure = extract_structure
        self.extract_dependencies = extract_dependencies
        self.extract_comments = extract_comments
        self.highlight_syntax = highlight_syntax and PYGMENTS_AVAILABLE
    
    def process(self, content: Any, metadata: Dict[str, Any] = None, **kwargs) -> Dict[str, Any]:
        """
        Process a code file.
        
        Args:
            content: Code content (string, bytes, or file path)
            metadata: Document metadata
            **kwargs: Additional processing options
            
        Returns:
            Processing results including extracted structure and text
        """
        if metadata is None:
            metadata = {}
        
        # Prepare code content for processing
        code_content, language = self._prepare_content(content, metadata.get('file_path'), metadata.get('language'))
        
        # Update metadata with detected language
        metadata['language'] = language
        metadata['content_type'] = f'text/{language}'
        
        # Extract structure if requested
        structure = {}
        if self.extract_structure:
            structure = self._extract_structure(code_content, language)
            
            # Add structure summary to metadata
            if structure:
                for key, items in structure.items():
                    if items:
                        metadata[f'{key}_count'] = len(items)
        
        # Extract dependencies if requested
        dependencies = []
        if self.extract_dependencies:
            dependencies = self._extract_dependencies(code_content, language)
            
            # Add dependencies to metadata
            if dependencies:
                metadata['dependencies_count'] = len(dependencies)
        
        # Extract comments if requested
        comments = []
        if self.extract_comments:
            comments = self._extract_comments(code_content, language)
            
            # Add comments to metadata
            if comments:
                metadata['comments_count'] = len(comments)
        
        # Perform syntax highlighting if requested
        highlighted_code = None
        if self.highlight_syntax:
            highlighted_code = self._highlight_syntax(code_content, language)
        
        # Create chunks based on the code structure
        chunks = self.create_chunks(code_content, structure=structure, language=language, **kwargs)
        
        # Prepare result
        result = {
            'chunks': chunks,
            'extracted_text': code_content,
            'metadata': metadata
        }
        
        # Add structure if extracted
        if structure:
            result['structure'] = structure
            
        # Add dependencies if extracted
        if dependencies:
            result['dependencies'] = dependencies
            
        # Add comments if extracted
        if comments:
            result['comments'] = comments
            
        # Add highlighted code if generated
        if highlighted_code:
            result['highlighted_code'] = highlighted_code
        
        return result
    
    def _prepare_content(self, content: Any, file_path: Optional[str] = None, language: Optional[str] = None) -> Tuple[str, str]:
        """
        Prepare code content for processing and detect language.
        
        Args:
            content: Code content (string, bytes, or file path)
            file_path: Path to the file (optional, used for language detection)
            language: Language identifier (optional, overrides detection)
            
        Returns:
            Tuple of (code content as string, detected language)
        """
        # Get content as string
        if isinstance(content, bytes):
            code_content = content.decode('utf-8', errors='replace')
        elif isinstance(content, str):
            if Path(content).exists() and file_path is None:
                # Content is a file path
                file_path = content
                with open(content, 'r', encoding='utf-8', errors='replace') as f:
                    code_content = f.read()
            else:
                # Content is the actual code
                code_content = content
        elif hasattr(content, 'read'):
            # File-like object
            code_content = content.read()
            if isinstance(code_content, bytes):
                code_content = code_content.decode('utf-8', errors='replace')
        else:
            raise ValueError(f"Unsupported content type: {type(content)}")
        
        # Detect language
        detected_language = language
        
        if not detected_language and file_path:
            # Try to detect from file extension
            ext = Path(file_path).suffix.lower()
            detected_language = self.EXTENSION_TO_LANGUAGE.get(ext)
        
        if not detected_language and PYGMENTS_AVAILABLE:
            # Try to detect using Pygments
            try:
                if file_path:
                    lexer = get_lexer_for_filename(file_path, code=code_content)
                else:
                    lexer = pygments.lexers.guess_lexer(code_content)
                
                detected_language = lexer.aliases[0]
            except Exception as e:
                logger.warning(f"Failed to detect language using Pygments: {e}")
        
        # Default to plaintext if detection failed
        if not detected_language:
            detected_language = 'plaintext'
        
        return code_content, detected_language
    
    def _extract_structure(self, code_content: str, language: str) -> Dict[str, List[Dict[str, Any]]]:
        """
        Extract code structure (functions, classes, etc.).
        
        Args:
            code_content: Code content as string
            language: Programming language
            
        Returns:
            Dictionary of extracted structure elements
        """
        structure = {}
        
        # Get language-specific patterns
        patterns = self.LANGUAGE_PATTERNS.get(language, {})
        
        # Extract each type of structure element
        for element_type, pattern in patterns.items():
            if element_type == 'comment':  # Skip comment pattern here
                continue
                
            matches = []
            for match in re.finditer(pattern, code_content, re.MULTILINE):
                # Get the line number
                line_number = code_content[:match.start()].count('\n') + 1
                
                # Get the matched name (first capturing group)
                name = next((group for group in match.groups() if group), '')
                
                # Get the context (surrounding lines)
                lines = code_content.split('\n')
                start_line = max(0, line_number - 2)
                end_line = min(len(lines), line_number + 2)
                context = '\n'.join(lines[start_line:end_line])
                
                matches.append({
                    'name': name,
                    'line': line_number,
                    'start': match.start(),
                    'end': match.end(),
                    'context': context
                })
            
            if matches:
                structure[element_type] = matches
        
        return structure
    
    def _extract_dependencies(self, code_content: str, language: str) -> List[Dict[str, Any]]:
        """
        Extract dependencies (imports, includes, etc.).
        
        Args:
            code_content: Code content as string
            language: Programming language
            
        Returns:
            List of extracted dependencies
        """
        dependencies = []
        
        # Get language-specific patterns
        patterns = self.LANGUAGE_PATTERNS.get(language, {})
        
        # Extract dependencies based on language
        if language in ['python', 'javascript', 'typescript', 'java', 'go', 'rust']:
            pattern_key = 'import' if language != 'rust' else 'use'
            if pattern_key in patterns:
                for match in re.finditer(patterns[pattern_key], code_content, re.MULTILINE):
                    # Get the line number
                    line_number = code_content[:match.start()].count('\n') + 1
                    
                    # Process the match based on language
                    if language == 'python':
                        module = match.group(1) or ''
                        imports = match.group(2) or ''
                        dependencies.append({
                            'type': 'import',
                            'module': module,
                            'imports': imports,
                            'line': line_number
                        })
                    elif language in ['javascript', 'typescript']:
                        source = match.group(4) or ''
                        dependencies.append({
                            'type': 'import',
                            'source': source,
                            'line': line_number
                        })
                    elif language == 'java':
                        package = match.group(1) or ''
                        dependencies.append({
                            'type': 'import',
                            'package': package,
                            'line': line_number
                        })
                    elif language == 'go':
                        package = match.group(1) or ''
                        dependencies.append({
                            'type': 'import',
                            'package': package,
                            'line': line_number
                        })
                    elif language == 'rust':
                        path = match.group(1) or ''
                        dependencies.append({
                            'type': 'use',
                            'path': path,
                            'line': line_number
                        })
        elif language in ['c', 'cpp']:
            for match in re.finditer(patterns['include'], code_content, re.MULTILINE):
                # Get the line number
                line_number = code_content[:match.start()].count('\n') + 1
                
                header = match.group(1) or ''
                dependencies.append({
                    'type': 'include',
                    'header': header,
                    'line': line_number
                })
        
        return dependencies
    
    def _extract_comments(self, code_content: str, language: str) -> List[Dict[str, Any]]:
        """
        Extract comments and docstrings.
        
        Args:
            code_content: Code content as string
            language: Programming language
            
        Returns:
            List of extracted comments
        """
        comments = []
        
        # Get language-specific patterns
        patterns = self.LANGUAGE_PATTERNS.get(language, {})
        
        # Extract comments
        if 'comment' in patterns:
            for match in re.finditer(patterns['comment'], code_content, re.MULTILINE):
                # Get the line number
                line_number = code_content[:match.start()].count('\n') + 1
                
                # Get the comment text
                text = match.group(0).strip()
                
                # Skip empty comments
                if not text or (language in ['python'] and text == '#'):
                    continue
                
                # Clean up the comment text
                if language in ['python']:
                    text = text.lstrip('#').strip()
                elif language in ['javascript', 'typescript', 'java', 'c', 'cpp', 'go', 'rust']:
                    if text.startswith('//'):
                        text = text[2:].strip()
                    elif text.startswith('/*') and text.endswith('*/'):
                        text = text[2:-2].strip()
                
                comments.append({
                    'type': 'comment',
                    'text': text,
                    'line': line_number
                })
        
        # Extract Python docstrings
        if language == 'python' and 'docstring' in patterns:
            for match in re.finditer(patterns['docstring'], code_content, re.MULTILINE):
                # Get the line number
                line_number = code_content[:match.start()].count('\n') + 1
                
                # Get the docstring text
                text = match.group(0).strip()
                
                # Clean up the docstring text
                if text.startswith('"""') and text.endswith('"""'):
                    text = text[3:-3].strip()
                elif text.startswith("'''") and text.endswith("'''"):
                    text = text[3:-3].strip()
                
                comments.append({
                    'type': 'docstring',
                    'text': text,
                    'line': line_number
                })
        
        return comments
    
    def _highlight_syntax(self, code_content: str, language: str) -> Optional[str]:
        """
        Perform syntax highlighting.
        
        Args:
            code_content: Code content as string
            language: Programming language
            
        Returns:
            HTML with syntax highlighting or None if highlighting failed
        """
        if not PYGMENTS_AVAILABLE:
            return None
        
        try:
            # Get lexer for the language
            try:
                lexer = get_lexer_by_name(language)
            except pygments.util.ClassNotFound:
                # Try with common aliases
                language_aliases = {
                    'javascript': 'js',
                    'typescript': 'ts',
                    'python': 'py',
                }
                alias = language_aliases.get(language)
                if alias:
                    try:
                        lexer = get_lexer_by_name(alias)
                    except pygments.util.ClassNotFound:
                        return None
                else:
                    return None
            
            # Highlight code
            from pygments.formatters import HtmlFormatter
            formatter = HtmlFormatter(linenos=True, cssclass="source")
            highlighted = pygments.highlight(code_content, lexer, formatter)
            
            return highlighted
        except Exception as e:
            logger.warning(f"Failed to highlight syntax: {e}")
            return None
    
    def create_chunks(self, text: str, structure: Dict[str, List[Dict[str, Any]]] = None, 
                     language: str = None, **kwargs) -> List[Dict[str, Any]]:
        """
        Create chunks from code, using structure information if available.
        
        Args:
            text: Code content
            structure: Code structure information
            language: Programming language
            **kwargs: Additional chunking options
            
        Returns:
            List of code chunks
        """
        chunks = []
        
        # If we have structure information, use it for structure-aware chunking
        if structure and language:
            # Combine all structure elements for sorting by position
            all_elements = []
            for element_type, elements in structure.items():
                for element in elements:
                    all_elements.append({
                        'type': element_type,
                        'name': element.get('name', ''),
                        'start': element.get('start', 0),
                        'end': element.get('end', 0),
                        'line': element.get('line', 0)
                    })
            
            # Sort elements by start position
            all_elements.sort(key=lambda x: x['start'])
            
            # Create chunks based on structure elements
            if all_elements:
                # Create chunks for each significant code section
                for i, element in enumerate(all_elements):
                    # Determine the end of this chunk
                    if i < len(all_elements) - 1:
                        next_start = all_elements[i + 1]['start']
                    else:
                        next_start = len(text)
                    
                    # Extract the chunk text
                    chunk_text = text[element['start']:next_start].strip()
                    
                    # Skip empty chunks
                    if not chunk_text:
                        continue
                    
                    # Create the chunk
                    chunk = {
                        'text': chunk_text,
                        'type': element['type'],
                        'metadata': {
                            'language': language,
                            'name': element['name'],
                            'line': element['line']
                        }
                    }
                    chunks.append(chunk)
                
                return chunks
        
        # Fall back to standard chunking if we couldn't use structure
        # For code, we'll use smaller chunks than the default
        chunk_size = kwargs.get('chunk_size', 1000)
        chunk_overlap = kwargs.get('chunk_overlap', 100)
        
        # Split by lines first to avoid breaking in the middle of a line
        lines = text.split('\n')
        current_chunk = []
        current_length = 0
        
        for line in lines:
            line_length = len(line) + 1  # +1 for the newline
            
            if current_length + line_length > chunk_size and current_chunk:
                # Create a chunk from the accumulated lines
                chunk_text = '\n'.join(current_chunk)
                chunks.append({
                    'text': chunk_text,
                    'type': 'code',
                    'metadata': {'language': language} if language else {}
                })
                
                # Start a new chunk with overlap
                overlap_lines = []
                overlap_length = 0
                for prev_line in reversed(current_chunk):
                    if overlap_length + len(prev_line) + 1 <= chunk_overlap:
                        overlap_lines.insert(0, prev_line)
                        overlap_length += len(prev_line) + 1
                    else:
                        break
                
                current_chunk = overlap_lines
                current_length = overlap_length
            
            current_chunk.append(line)
            current_length += line_length
        
        # Add the final chunk if there's anything left
        if current_chunk:
            chunk_text = '\n'.join(current_chunk)
            chunks.append({
                'text': chunk_text,
                'type': 'code',
                'metadata': {'language': language} if language else {}
            })
        
        return chunks
    
    def store_in_graph(self, document_id: str, metadata: Dict[str, Any], 
                      chunks: List[Dict[str, Any]], **kwargs) -> None:
        """
        Store code document in graph database.
        
        Args:
            document_id: Document ID
            metadata: Document metadata
            chunks: Document chunks
            **kwargs: Additional storage options
        """
        # Get language from metadata
        language = metadata.get('language', 'unknown')
        
        # Add code-specific metadata
        metadata['content_type'] = f'text/{language}'
        
        # Store document node
        doc_properties = {
            'id': document_id,
            'content_type': f'text/{language}',
            'language': language,
            **metadata
        }
        
        # Create document node
        self.graph_db.create_node('Document', doc_properties)
        
        # Store each chunk
        for i, chunk in enumerate(chunks):
            chunk_id = f"{document_id}_chunk_{i}"
            chunk_type = chunk.get('type', 'code')
            
            # Create chunk node
            chunk_properties = {
                'id': chunk_id,
                'text': chunk['text'],
                'type': chunk_type,
                'index': i,
                **chunk.get('metadata', {})
            }
            self.graph_db.create_node('Chunk', chunk_properties)
            
            # Connect chunk to document
            self.graph_db.create_relationship(
                'Document', {'id': document_id},
                'HAS_CHUNK', {},
                'Chunk', {'id': chunk_id}
            )
            
            # Create special relationships based on chunk type
            if chunk_type in ['function', 'class', 'struct', 'interface']:
                # Create a node for the code element
                element_name = chunk.get('metadata', {}).get('name', '')
                if element_name:
                    element_id = f"{document_id}_{chunk_type}_{element_name}"
                    self.graph_db.create_node(chunk_type.capitalize(), {
                        'id': element_id,
                        'name': element_name,
                        'language': language
                    })
                    
                    # Connect chunk to element
                    self.graph_db.create_relationship(
                        chunk_type.capitalize(), {'id': element_id},
                        'HAS_IMPLEMENTATION', {},
                        'Chunk', {'id': chunk_id}
                    )
                    
                    # Connect document to element
                    self.graph_db.create_relationship(
                        'Document', {'id': document_id},
                        f'HAS_{chunk_type.upper()}', {},
                        chunk_type.capitalize(), {'id': element_id}
                    )
        
        # Store dependencies if available
        if 'dependencies' in kwargs:
            for i, dep in enumerate(kwargs['dependencies']):
                dep_id = f"{document_id}_dependency_{i}"
                
                # Create dependency node
                dep_properties = {
                    'id': dep_id,
                    **dep
                }
                self.graph_db.create_node('Dependency', dep_properties)
                
                # Connect document to dependency
                self.graph_db.create_relationship(
                    'Document', {'id': document_id},
                    'DEPENDS_ON', {},
                    'Dependency', {'id': dep_id}
                )
    
    def store_in_vector_db(self, document_id: str, metadata: Dict[str, Any],
                          chunks: List[Dict[str, Any]], **kwargs) -> None:
        """
        Store code document in vector database.
        
        Args:
            document_id: Document ID
            metadata: Document metadata
            chunks: Document chunks
            **kwargs: Additional storage options
        """
        # Get language from metadata
        language = metadata.get('language', 'unknown')
        
        # Add code-specific metadata
        metadata['content_type'] = f'text/{language}'
        
        # Store each chunk with its embeddings
        for i, chunk in enumerate(chunks):
            chunk_id = f"{document_id}_chunk_{i}"
            chunk_text = chunk['text']
            
            # Get embeddings for the chunk
            embeddings = self.get_embeddings(chunk_text)
            
            # Prepare chunk metadata
            chunk_metadata = {
                'document_id': document_id,
                'chunk_id': chunk_id,
                'chunk_index': i,
                'chunk_type': chunk.get('type', 'code'),
                'language': language,
                **metadata,
                **chunk.get('metadata', {})
            }
            
            # Store in vector database
            self.vector_db.add_vectors(
                collection_name=kwargs.get('collection_name', 'documents'),
                vectors=[(chunk_id, embeddings, chunk_metadata)],
                batch_size=kwargs.get('batch_size', 100)
            ) 