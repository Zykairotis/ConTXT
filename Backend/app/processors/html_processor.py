"""
HTML document processor.

This module provides a processor for HTML documents that extracts text,
structure, links, and other elements from HTML content.
"""
import logging
import re
from typing import Dict, Any, List, Optional, Tuple, Set
from urllib.parse import urljoin, urlparse

# HTML processing libraries
try:
    from bs4 import BeautifulSoup
    BS4_AVAILABLE = True
except ImportError:
    BS4_AVAILABLE = False

try:
    import html2text
    HTML2TEXT_AVAILABLE = True
except ImportError:
    HTML2TEXT_AVAILABLE = False

from app.processors.base import BaseProcessor

logger = logging.getLogger(__name__)

class HTMLProcessor(BaseProcessor):
    """
    Processor for HTML documents.
    
    This processor extracts text, structure, links, and other elements from HTML content.
    It uses BeautifulSoup for parsing and html2text for conversion to plain text.
    """
    
    # HTML elements that typically represent standalone sections
    SECTION_ELEMENTS = {
        'article', 'section', 'div', 'main', 'aside', 'header', 'footer',
        'nav', 'form'
    }
    
    # HTML elements that typically represent headings
    HEADING_ELEMENTS = {'h1', 'h2', 'h3', 'h4', 'h5', 'h6'}
    
    # HTML elements to extract as metadata
    METADATA_ELEMENTS = {
        'title', 'meta', 'link[rel="canonical"]', 'link[rel="alternate"]',
        'meta[property^="og:"]', 'meta[name^="twitter:"]', 'meta[name="description"]'
    }
    
    def __init__(self, 
                 extract_links: bool = True,
                 extract_images: bool = True,
                 extract_tables: bool = True,
                 extract_metadata: bool = True,
                 clean_html: bool = True,
                 base_url: Optional[str] = None,
                 **kwargs):
        """
        Initialize the HTML processor.
        
        Args:
            extract_links: Whether to extract links from the HTML
            extract_images: Whether to extract image information
            extract_tables: Whether to extract tables
            extract_metadata: Whether to extract metadata (title, description, etc.)
            clean_html: Whether to clean the HTML (remove scripts, styles, etc.)
            base_url: Base URL for resolving relative URLs
            **kwargs: Additional options for the base processor
        """
        super().__init__(**kwargs)
        
        if not BS4_AVAILABLE:
            raise ImportError(
                "BeautifulSoup is required for HTML processing. "
                "Please install it with: pip install beautifulsoup4"
            )
        
        self.extract_links = extract_links
        self.extract_images = extract_images
        self.extract_tables = extract_tables
        self.extract_metadata = extract_metadata
        self.clean_html = clean_html
        self.base_url = base_url
    
    def process(self, content: Any, metadata: Dict[str, Any] = None, **kwargs) -> Dict[str, Any]:
        """
        Process an HTML document.
        
        Args:
            content: HTML content (string or bytes)
            metadata: Document metadata
            **kwargs: Additional processing options
            
        Returns:
            Processing results including extracted text, structure, and links
        """
        if metadata is None:
            metadata = {}
        
        # Prepare HTML content for processing
        html_content = self._prepare_content(content)
        
        # Parse HTML with BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Clean HTML if requested
        if self.clean_html:
            self._clean_html(soup)
        
        # Extract metadata if requested
        if self.extract_metadata:
            page_metadata = self._extract_metadata(soup)
            metadata.update(page_metadata)
        
        # Extract links if requested
        links = []
        if self.extract_links:
            links = self._extract_links(soup)
            metadata['links_count'] = len(links)
        
        # Extract images if requested
        images = []
        if self.extract_images:
            images = self._extract_images(soup)
            metadata['images_count'] = len(images)
        
        # Extract tables if requested
        tables = []
        if self.extract_tables:
            tables = self._extract_tables(soup)
            metadata['tables_count'] = len(tables)
        
        # Extract text and structure
        extracted_text, structure = self._extract_text_and_structure(soup)
        
        # Create chunks based on the document structure
        chunks = self.create_chunks(extracted_text, structure=structure, **kwargs)
        
        # Prepare result
        result = {
            'chunks': chunks,
            'extracted_text': extracted_text,
            'metadata': metadata
        }
        
        # Add document structure if available
        if structure:
            result['structure'] = structure
            
        # Add links if extracted
        if links:
            result['links'] = links
            
        # Add images if extracted
        if images:
            result['images'] = images
            
        # Add tables if extracted
        if tables:
            result['tables'] = tables
        
        return result
    
    def _prepare_content(self, content: Any) -> str:
        """
        Prepare HTML content for processing.
        
        Args:
            content: HTML content (string or bytes)
            
        Returns:
            HTML content as string
        """
        if isinstance(content, bytes):
            return content.decode('utf-8', errors='replace')
        elif isinstance(content, str):
            return content
        elif hasattr(content, 'read'):
            # File-like object
            return content.read().decode('utf-8', errors='replace') if isinstance(content.read(), bytes) else content.read()
        else:
            raise ValueError(f"Unsupported content type: {type(content)}")
    
    def _clean_html(self, soup: BeautifulSoup) -> None:
        """
        Clean HTML by removing scripts, styles, and comments.
        
        Args:
            soup: BeautifulSoup object
        """
        # Remove script tags
        for script in soup.find_all('script'):
            script.decompose()
        
        # Remove style tags
        for style in soup.find_all('style'):
            style.decompose()
        
        # Remove comments
        for comment in soup.find_all(string=lambda text: isinstance(text, str) and text.strip().startswith('<!--')):
            comment.extract()
    
    def _extract_metadata(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """
        Extract metadata from HTML.
        
        Args:
            soup: BeautifulSoup object
            
        Returns:
            Dictionary of metadata
        """
        metadata = {}
        
        # Extract title
        title_tag = soup.find('title')
        if title_tag and title_tag.string:
            metadata['title'] = title_tag.string.strip()
        
        # Extract meta description
        description_tag = soup.find('meta', attrs={'name': 'description'})
        if description_tag and description_tag.get('content'):
            metadata['description'] = description_tag['content'].strip()
        
        # Extract Open Graph metadata
        og_tags = soup.find_all('meta', attrs={'property': re.compile(r'^og:')})
        if og_tags:
            og_metadata = {}
            for tag in og_tags:
                if tag.get('content'):
                    property_name = tag['property'][3:]  # Remove 'og:' prefix
                    og_metadata[property_name] = tag['content'].strip()
            
            if og_metadata:
                metadata['open_graph'] = og_metadata
        
        # Extract Twitter card metadata
        twitter_tags = soup.find_all('meta', attrs={'name': re.compile(r'^twitter:')})
        if twitter_tags:
            twitter_metadata = {}
            for tag in twitter_tags:
                if tag.get('content'):
                    property_name = tag['name'][8:]  # Remove 'twitter:' prefix
                    twitter_metadata[property_name] = tag['content'].strip()
            
            if twitter_metadata:
                metadata['twitter_card'] = twitter_metadata
        
        # Extract canonical URL
        canonical_tag = soup.find('link', attrs={'rel': 'canonical'})
        if canonical_tag and canonical_tag.get('href'):
            metadata['canonical_url'] = canonical_tag['href'].strip()
        
        return metadata
    
    def _extract_links(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """
        Extract links from HTML.
        
        Args:
            soup: BeautifulSoup object
            
        Returns:
            List of extracted links with metadata
        """
        links = []
        seen_urls = set()
        
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href'].strip()
            
            # Skip empty, javascript, and anchor links
            if not href or href.startswith('javascript:') or href == '#':
                continue
            
            # Resolve relative URLs if base_url is provided
            if self.base_url and not urlparse(href).netloc:
                href = urljoin(self.base_url, href)
            
            # Skip duplicates
            if href in seen_urls:
                continue
            
            seen_urls.add(href)
            
            # Extract link text and title
            text = a_tag.get_text().strip()
            title = a_tag.get('title', '').strip()
            
            links.append({
                'url': href,
                'text': text,
                'title': title if title else None,
                'is_external': bool(urlparse(href).netloc) if self.base_url else None
            })
        
        return links
    
    def _extract_images(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """
        Extract images from HTML.
        
        Args:
            soup: BeautifulSoup object
            
        Returns:
            List of extracted images with metadata
        """
        images = []
        seen_urls = set()
        
        for img_tag in soup.find_all('img'):
            src = img_tag.get('src', '').strip()
            
            # Skip empty sources
            if not src:
                continue
            
            # Resolve relative URLs if base_url is provided
            if self.base_url and not urlparse(src).netloc:
                src = urljoin(self.base_url, src)
            
            # Skip duplicates
            if src in seen_urls:
                continue
            
            seen_urls.add(src)
            
            # Extract image metadata
            alt = img_tag.get('alt', '').strip()
            title = img_tag.get('title', '').strip()
            width = img_tag.get('width')
            height = img_tag.get('height')
            
            images.append({
                'url': src,
                'alt': alt if alt else None,
                'title': title if title else None,
                'width': int(width) if width and width.isdigit() else None,
                'height': int(height) if height and height.isdigit() else None
            })
        
        return images
    
    def _extract_tables(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """
        Extract tables from HTML.
        
        Args:
            soup: BeautifulSoup object
            
        Returns:
            List of extracted tables with metadata
        """
        tables = []
        
        for i, table_tag in enumerate(soup.find_all('table')):
            # Extract table caption
            caption = table_tag.find('caption')
            caption_text = caption.get_text().strip() if caption else None
            
            # Extract headers
            headers = []
            header_row = table_tag.find('thead')
            if header_row:
                for th in header_row.find_all('th'):
                    headers.append(th.get_text().strip())
            
            # Extract rows
            rows = []
            for tr in table_tag.find_all('tr'):
                row = [td.get_text().strip() for td in tr.find_all(['td', 'th'])]
                if row:  # Skip empty rows
                    rows.append(row)
            
            # Convert table to text
            table_text = ""
            if caption_text:
                table_text += f"{caption_text}\n\n"
            
            for row in rows:
                table_text += " | ".join(row) + "\n"
            
            tables.append({
                'index': i,
                'caption': caption_text,
                'headers': headers if headers else None,
                'rows': len(rows),
                'columns': len(headers) if headers else (len(rows[0]) if rows else 0),
                'text': table_text.strip()
            })
        
        return tables
    
    def _extract_text_and_structure(self, soup: BeautifulSoup) -> Tuple[str, Dict[str, Any]]:
        """
        Extract text and structure from HTML.
        
        Args:
            soup: BeautifulSoup object
            
        Returns:
            Tuple of (extracted text, structure dict)
        """
        # Extract structure
        structure = {
            'headings': [],
            'sections': []
        }
        
        # Extract headings
        for i, heading in enumerate(soup.find_all(self.HEADING_ELEMENTS)):
            heading_text = heading.get_text().strip()
            if heading_text:
                heading_level = int(heading.name[1])  # Extract number from h1, h2, etc.
                structure['headings'].append({
                    'text': heading_text,
                    'level': heading_level,
                    'index': i
                })
        
        # Extract sections
        for i, section in enumerate(soup.find_all(self.SECTION_ELEMENTS)):
            # Skip empty sections
            if not section.get_text().strip():
                continue
                
            # Get section heading if available
            section_heading = None
            for heading in section.find_all(self.HEADING_ELEMENTS, recursive=False):
                section_heading = heading.get_text().strip()
                break
            
            # Get section ID or class for identification
            section_id = section.get('id', '')
            section_class = ' '.join(section.get('class', []))
            
            structure['sections'].append({
                'heading': section_heading,
                'id': section_id if section_id else None,
                'class': section_class if section_class else None,
                'index': i
            })
        
        # Convert HTML to plain text
        if HTML2TEXT_AVAILABLE:
            # Use html2text for better formatting
            h = html2text.HTML2Text()
            h.ignore_links = False
            h.ignore_images = False
            h.ignore_tables = False
            h.body_width = 0  # No wrapping
            text = h.handle(str(soup))
        else:
            # Fallback to BeautifulSoup's get_text
            text = soup.get_text(separator='\n\n')
        
        return text, structure
    
    def create_chunks(self, text: str, structure: Dict[str, Any] = None, **kwargs) -> List[Dict[str, Any]]:
        """
        Create chunks from HTML text, using structure information if available.
        
        Args:
            text: Extracted text
            structure: Document structure information
            **kwargs: Additional chunking options
            
        Returns:
            List of text chunks
        """
        chunks = []
        
        # If we have headings, use them for structure-aware chunking
        if structure and structure.get('headings'):
            headings = structure['headings']
            
            # Use heading text as markers to split the text
            markers = []
            for heading in headings:
                heading_text = heading['text']
                # Look for the heading text or a markdown-style heading
                patterns = [
                    re.escape(heading_text),
                    re.escape(f"# {heading_text}"),
                    re.escape(f"## {heading_text}"),
                    re.escape(f"### {heading_text}"),
                    re.escape(f"#### {heading_text}")
                ]
                for pattern in patterns:
                    matches = list(re.finditer(pattern, text))
                    if matches:
                        for match in matches:
                            markers.append({
                                'text': heading_text,
                                'position': match.start(),
                                'level': heading['level']
                            })
                        break
            
            # Sort markers by position
            markers.sort(key=lambda x: x['position'])
            
            # Split text by markers
            if markers:
                current_pos = 0
                
                for i, marker in enumerate(markers):
                    marker_pos = marker['position']
                    
                    # Add the text before this marker if it's not the first marker
                    if i > 0 and marker_pos > current_pos:
                        prev_text = text[current_pos:marker_pos].strip()
                        if prev_text:
                            chunks.append({
                                'text': prev_text,
                                'type': 'section',
                                'metadata': {
                                    'heading': markers[i-1]['text'],
                                    'level': markers[i-1]['level']
                                }
                            })
                    
                    current_pos = marker_pos + len(marker['text'])
                
                # Add the final section
                if current_pos < len(text):
                    final_text = text[current_pos:].strip()
                    if final_text:
                        chunks.append({
                            'text': final_text,
                            'type': 'section',
                            'metadata': {
                                'heading': markers[-1]['text'],
                                'level': markers[-1]['level']
                            }
                        })
                
                return chunks
        
        # Fall back to standard chunking if we couldn't use structure
        return super().create_chunks(text, **kwargs)
    
    def store_in_graph(self, document_id: str, metadata: Dict[str, Any], 
                      chunks: List[Dict[str, Any]], **kwargs) -> None:
        """
        Store HTML document in graph database.
        
        Args:
            document_id: Document ID
            metadata: Document metadata
            chunks: Document chunks
            **kwargs: Additional storage options
        """
        # Add HTML-specific metadata
        metadata['content_type'] = 'text/html'
        
        # Store document node
        doc_properties = {
            'id': document_id,
            'content_type': 'text/html',
            **metadata
        }
        
        # Create document node
        self.graph_db.create_node('Document', doc_properties)
        
        # Store each chunk
        for i, chunk in enumerate(chunks):
            chunk_id = f"{document_id}_chunk_{i}"
            chunk_type = chunk.get('type', 'text')
            
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
            if chunk_type == 'section':
                heading = chunk.get('metadata', {}).get('heading')
                if heading:
                    # Create heading node if it doesn't exist
                    heading_id = f"{document_id}_heading_{heading}"
                    self.graph_db.create_node('Heading', {
                        'id': heading_id,
                        'text': heading,
                        'level': chunk.get('metadata', {}).get('level', 1)
                    })
                    
                    # Connect chunk to heading
                    self.graph_db.create_relationship(
                        'Heading', {'id': heading_id},
                        'CONTAINS', {},
                        'Chunk', {'id': chunk_id}
                    )
                    
                    # Connect document to heading
                    self.graph_db.create_relationship(
                        'Document', {'id': document_id},
                        'HAS_HEADING', {},
                        'Heading', {'id': heading_id}
                    )
        
        # Store links if available
        if 'links' in kwargs:
            for i, link in enumerate(kwargs['links']):
                link_id = f"{document_id}_link_{i}"
                
                # Create link node
                link_properties = {
                    'id': link_id,
                    'url': link['url'],
                    'text': link.get('text', ''),
                    'title': link.get('title', ''),
                    'is_external': link.get('is_external', False)
                }
                self.graph_db.create_node('Link', link_properties)
                
                # Connect document to link
                self.graph_db.create_relationship(
                    'Document', {'id': document_id},
                    'HAS_LINK', {},
                    'Link', {'id': link_id}
                )
    
    def store_in_vector_db(self, document_id: str, metadata: Dict[str, Any],
                          chunks: List[Dict[str, Any]], **kwargs) -> None:
        """
        Store HTML document in vector database.
        
        Args:
            document_id: Document ID
            metadata: Document metadata
            chunks: Document chunks
            **kwargs: Additional storage options
        """
        # Add HTML-specific metadata
        metadata['content_type'] = 'text/html'
        
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
                'chunk_type': chunk.get('type', 'text'),
                **metadata,
                **chunk.get('metadata', {})
            }
            
            # Store in vector database
            self.vector_db.add_vectors(
                collection_name=kwargs.get('collection_name', 'documents'),
                vectors=[(chunk_id, embeddings, chunk_metadata)],
                batch_size=kwargs.get('batch_size', 100)
            ) 