"""
PDF document processor.

This module provides a processor for PDF documents that extracts text,
structure, and images from PDF files.
"""
import logging
import io
import tempfile
from typing import Dict, Any, List, Optional, Tuple, BinaryIO
import base64
from pathlib import Path

# PDF processing libraries
try:
    import fitz  # PyMuPDF
    PYMUPDF_AVAILABLE = True
except ImportError:
    PYMUPDF_AVAILABLE = False
    
try:
    from pdfminer.high_level import extract_text as pdfminer_extract_text
    from pdfminer.layout import LAParams
    PDFMINER_AVAILABLE = True
except ImportError:
    PDFMINER_AVAILABLE = False

from app.processors.base import BaseProcessor
from app.processors.image_processor import ImageProcessor

logger = logging.getLogger(__name__)

class PDFProcessor(BaseProcessor):
    """
    Processor for PDF documents.
    
    This processor extracts text, structure, and images from PDF files.
    It uses PyMuPDF (fitz) as the primary engine with fallback to pdfminer.six.
    """
    
    def __init__(self, 
                 extract_images: bool = True,
                 ocr_images: bool = False,
                 extract_tables: bool = True,
                 detect_headers: bool = True,
                 **kwargs):
        """
        Initialize the PDF processor.
        
        Args:
            extract_images: Whether to extract images from the PDF
            ocr_images: Whether to run OCR on extracted images
            extract_tables: Whether to extract tables from the PDF
            detect_headers: Whether to detect headers and structure
            **kwargs: Additional options for the base processor
        """
        super().__init__(**kwargs)
        
        if not PYMUPDF_AVAILABLE and not PDFMINER_AVAILABLE:
            raise ImportError(
                "No PDF processing library available. "
                "Please install PyMuPDF (pip install pymupdf) or "
                "pdfminer.six (pip install pdfminer.six)."
            )
        
        self.extract_images = extract_images
        self.ocr_images = ocr_images
        self.extract_tables = extract_tables
        self.detect_headers = detect_headers
        
        # Create an image processor for handling extracted images
        if extract_images:
            self.image_processor = ImageProcessor(**kwargs)
    
    def process(self, content: Any, metadata: Dict[str, Any] = None, **kwargs) -> Dict[str, Any]:
        """
        Process a PDF document.
        
        Args:
            content: PDF content (bytes, file-like object, or path)
            metadata: Document metadata
            **kwargs: Additional processing options
            
        Returns:
            Processing results including extracted text, structure, and images
        """
        if metadata is None:
            metadata = {}
        
        # Prepare PDF content for processing
        pdf_content = self._prepare_content(content)
        
        # Extract text and structure
        extracted_text, structure = self._extract_text_and_structure(pdf_content)
        
        # Create chunks based on the document structure
        chunks = self.create_chunks(extracted_text, structure=structure, **kwargs)
        
        # Extract and process images if enabled
        images = []
        if self.extract_images:
            images = self._extract_images(pdf_content)
            
            # Process images with OCR if enabled
            if self.ocr_images and images:
                for i, img_data in enumerate(images):
                    img_result = self.image_processor.process(
                        img_data['image'], 
                        metadata={'page': img_data['page'], 'index': i}
                    )
                    
                    # Add OCR text to the image data
                    if 'extracted_text' in img_result:
                        images[i]['ocr_text'] = img_result['extracted_text']
                        
                        # Add image text as additional chunks
                        if img_result['extracted_text'].strip():
                            img_chunk = {
                                'text': img_result['extracted_text'],
                                'type': 'image_text',
                                'metadata': {
                                    'page': img_data['page'],
                                    'image_index': i
                                }
                            }
                            chunks.append(img_chunk)
        
        # Extract tables if enabled
        tables = []
        if self.extract_tables:
            tables = self._extract_tables(pdf_content)
            
            # Add table text as additional chunks
            for i, table in enumerate(tables):
                if 'text' in table and table['text'].strip():
                    table_chunk = {
                        'text': table['text'],
                        'type': 'table',
                        'metadata': {
                            'page': table['page'],
                            'table_index': i
                        }
                    }
                    chunks.append(table_chunk)
        
        # Prepare result
        result = {
            'chunks': chunks,
            'extracted_text': extracted_text,
            'metadata': metadata
        }
        
        # Add document structure if available
        if structure:
            result['structure'] = structure
            
        # Add images if extracted
        if images:
            result['images'] = images
            
        # Add tables if extracted
        if tables:
            result['tables'] = tables
        
        return result
    
    def _prepare_content(self, content: Any) -> bytes:
        """
        Prepare PDF content for processing.
        
        Args:
            content: PDF content (bytes, file-like object, or path)
            
        Returns:
            PDF content as bytes
        """
        if isinstance(content, bytes):
            return content
        elif isinstance(content, (str, Path)):
            with open(content, 'rb') as f:
                return f.read()
        elif hasattr(content, 'read'):
            # File-like object
            return content.read()
        else:
            raise ValueError(f"Unsupported content type: {type(content)}")
    
    def _extract_text_and_structure(self, pdf_content: bytes) -> Tuple[str, Dict[str, Any]]:
        """
        Extract text and structure from a PDF document.
        
        Args:
            pdf_content: PDF content as bytes
            
        Returns:
            Tuple of (extracted text, structure dict)
        """
        if PYMUPDF_AVAILABLE:
            return self._extract_with_pymupdf(pdf_content)
        elif PDFMINER_AVAILABLE:
            return self._extract_with_pdfminer(pdf_content)
        else:
            raise ImportError("No PDF processing library available")
    
    def _extract_with_pymupdf(self, pdf_content: bytes) -> Tuple[str, Dict[str, Any]]:
        """
        Extract text and structure using PyMuPDF.
        
        Args:
            pdf_content: PDF content as bytes
            
        Returns:
            Tuple of (extracted text, structure dict)
        """
        full_text = []
        structure = {
            'pages': [],
            'toc': [],
            'headers': []
        }
        
        # Create a temporary file for PyMuPDF
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp:
            tmp.write(pdf_content)
            tmp_path = tmp.name
        
        try:
            # Open the PDF with PyMuPDF
            doc = fitz.open(tmp_path)
            
            # Extract table of contents if available
            toc = doc.get_toc()
            if toc:
                structure['toc'] = [
                    {'level': level, 'title': title, 'page': page} 
                    for level, title, page in toc
                ]
            
            # Process each page
            for page_num, page in enumerate(doc):
                # Extract text
                page_text = page.get_text()
                full_text.append(page_text)
                
                # Extract page structure
                page_structure = {
                    'number': page_num + 1,
                    'width': page.rect.width,
                    'height': page.rect.height
                }
                
                # Detect headers if enabled
                if self.detect_headers:
                    blocks = page.get_text("dict")["blocks"]
                    headers = []
                    
                    for block in blocks:
                        if "lines" in block:
                            for line in block["lines"]:
                                if line["spans"]:
                                    # Check if this might be a header (larger font, bold, etc.)
                                    for span in line["spans"]:
                                        if span["size"] > 12 or "bold" in span.get("font", "").lower():
                                            header_text = span["text"].strip()
                                            if header_text:
                                                headers.append({
                                                    'text': header_text,
                                                    'page': page_num + 1,
                                                    'font_size': span["size"],
                                                    'is_bold': "bold" in span.get("font", "").lower()
                                                })
                                            break
                    
                    if headers:
                        page_structure['headers'] = headers
                        structure['headers'].extend(headers)
                
                structure['pages'].append(page_structure)
            
            # Close the document
            doc.close()
            
        finally:
            # Clean up the temporary file
            Path(tmp_path).unlink(missing_ok=True)
        
        return "\n\n".join(full_text), structure
    
    def _extract_with_pdfminer(self, pdf_content: bytes) -> Tuple[str, Dict[str, Any]]:
        """
        Extract text and structure using pdfminer.six.
        
        Args:
            pdf_content: PDF content as bytes
            
        Returns:
            Tuple of (extracted text, structure dict)
        """
        # Basic structure without detailed info
        structure = {
            'pages': [],
            'headers': []
        }
        
        # Extract text with pdfminer
        text = pdfminer_extract_text(io.BytesIO(pdf_content), laparams=LAParams())
        
        return text, structure
    
    def _extract_images(self, pdf_content: bytes) -> List[Dict[str, Any]]:
        """
        Extract images from a PDF document.
        
        Args:
            pdf_content: PDF content as bytes
            
        Returns:
            List of extracted images with metadata
        """
        if not PYMUPDF_AVAILABLE:
            logger.warning("PyMuPDF not available, skipping image extraction")
            return []
        
        images = []
        
        # Create a temporary file for PyMuPDF
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp:
            tmp.write(pdf_content)
            tmp_path = tmp.name
        
        try:
            # Open the PDF with PyMuPDF
            doc = fitz.open(tmp_path)
            
            # Process each page
            for page_num, page in enumerate(doc):
                # Extract images
                image_list = page.get_images(full=True)
                
                for img_index, img in enumerate(image_list):
                    xref = img[0]
                    base_image = doc.extract_image(xref)
                    
                    if base_image:
                        image_bytes = base_image["image"]
                        image_ext = base_image["ext"]
                        
                        # Encode image as base64 for storage
                        image_b64 = base64.b64encode(image_bytes).decode('utf-8')
                        
                        images.append({
                            'page': page_num + 1,
                            'index': img_index,
                            'width': base_image.get('width'),
                            'height': base_image.get('height'),
                            'format': image_ext,
                            'image': image_bytes,  # Raw bytes for processing
                            'image_b64': image_b64  # Base64 for storage
                        })
            
            # Close the document
            doc.close()
            
        finally:
            # Clean up the temporary file
            Path(tmp_path).unlink(missing_ok=True)
        
        return images
    
    def _extract_tables(self, pdf_content: bytes) -> List[Dict[str, Any]]:
        """
        Extract tables from a PDF document.
        
        Args:
            pdf_content: PDF content as bytes
            
        Returns:
            List of extracted tables with metadata
        """
        # For now, use a simple heuristic approach
        # A more robust solution would use a dedicated PDF table extraction library
        tables = []
        
        if not PYMUPDF_AVAILABLE:
            return tables
        
        # Create a temporary file for PyMuPDF
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp:
            tmp.write(pdf_content)
            tmp_path = tmp.name
        
        try:
            # Open the PDF with PyMuPDF
            doc = fitz.open(tmp_path)
            
            # Process each page
            for page_num, page in enumerate(doc):
                # Simple table detection based on text blocks
                blocks = page.get_text("blocks")
                
                for block_idx, block in enumerate(blocks):
                    block_text = block[4]
                    
                    # Heuristic: Check if the block might be a table
                    # (contains multiple lines with similar structure)
                    lines = block_text.split('\n')
                    if len(lines) > 3:  # At least 3 rows
                        # Check if lines have similar structure (e.g., same number of separators)
                        separators = ['\t', '  ', '|', ',']
                        
                        for sep in separators:
                            if all(sep in line for line in lines[:3]):  # First 3 lines contain separator
                                tables.append({
                                    'page': page_num + 1,
                                    'block': block_idx,
                                    'text': block_text,
                                    'separator': sep,
                                    'rows': len(lines)
                                })
                                break
            
            # Close the document
            doc.close()
            
        finally:
            # Clean up the temporary file
            Path(tmp_path).unlink(missing_ok=True)
        
        return tables
    
    def create_chunks(self, text: str, structure: Dict[str, Any] = None, **kwargs) -> List[Dict[str, Any]]:
        """
        Create chunks from PDF text, using structure information if available.
        
        Args:
            text: Extracted text
            structure: Document structure information
            **kwargs: Additional chunking options
            
        Returns:
            List of text chunks
        """
        chunks = []
        
        # If we have TOC or headers, use them for structure-aware chunking
        if structure and (structure.get('toc') or structure.get('headers')):
            # Combine TOC and headers for section detection
            sections = []
            
            if structure.get('toc'):
                for item in structure['toc']:
                    sections.append({
                        'title': item['title'],
                        'page': item['page'],
                        'level': item['level']
                    })
            
            if structure.get('headers'):
                for header in structure['headers']:
                    # Only add headers that aren't already in TOC
                    if not any(s['title'] == header['text'] for s in sections):
                        sections.append({
                            'title': header['text'],
                            'page': header['page'],
                            'level': 1  # Assume top-level for detected headers
                        })
            
            # Sort sections by page number
            sections.sort(key=lambda x: x['page'])
            
            # Split text by sections if we have sections
            if sections:
                # Use section titles as markers to split the text
                current_pos = 0
                
                for i, section in enumerate(sections):
                    section_title = section['title']
                    
                    # Find the section title in the text
                    section_pos = text.find(section_title, current_pos)
                    
                    if section_pos != -1:
                        # Add the text before this section if it's not the first section
                        if i > 0 and section_pos > current_pos:
                            prev_text = text[current_pos:section_pos].strip()
                            if prev_text:
                                chunks.append({
                                    'text': prev_text,
                                    'type': 'section',
                                    'metadata': {
                                        'section': sections[i-1]['title'],
                                        'level': sections[i-1]['level'],
                                        'page': sections[i-1]['page']
                                    }
                                })
                        
                        current_pos = section_pos + len(section_title)
                
                # Add the final section
                if current_pos < len(text):
                    final_text = text[current_pos:].strip()
                    if final_text:
                        chunks.append({
                            'text': final_text,
                            'type': 'section',
                            'metadata': {
                                'section': sections[-1]['title'] if sections else None,
                                'level': sections[-1]['level'] if sections else None,
                                'page': sections[-1]['page'] if sections else None
                            }
                        })
                
                return chunks
        
        # Fall back to standard chunking if we couldn't use structure
        return super().create_chunks(text, **kwargs)
    
    def store_in_graph(self, document_id: str, metadata: Dict[str, Any], 
                      chunks: List[Dict[str, Any]], **kwargs) -> None:
        """
        Store PDF document in graph database.
        
        Args:
            document_id: Document ID
            metadata: Document metadata
            chunks: Document chunks
            **kwargs: Additional storage options
        """
        # Add PDF-specific metadata
        metadata['content_type'] = 'application/pdf'
        
        # Store document node
        doc_properties = {
            'id': document_id,
            'content_type': 'application/pdf',
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
                section_title = chunk.get('metadata', {}).get('section')
                if section_title:
                    # Create section node if it doesn't exist
                    section_id = f"{document_id}_section_{section_title}"
                    self.graph_db.create_node('Section', {
                        'id': section_id,
                        'title': section_title,
                        'level': chunk.get('metadata', {}).get('level', 1)
                    })
                    
                    # Connect chunk to section
                    self.graph_db.create_relationship(
                        'Section', {'id': section_id},
                        'CONTAINS', {},
                        'Chunk', {'id': chunk_id}
                    )
                    
                    # Connect document to section
                    self.graph_db.create_relationship(
                        'Document', {'id': document_id},
                        'HAS_SECTION', {},
                        'Section', {'id': section_id}
                    )
            
            elif chunk_type == 'table':
                table_index = chunk.get('metadata', {}).get('table_index')
                if table_index is not None:
                    # Create table node
                    table_id = f"{document_id}_table_{table_index}"
                    self.graph_db.create_node('Table', {
                        'id': table_id,
                        'index': table_index,
                        'page': chunk.get('metadata', {}).get('page')
                    })
                    
                    # Connect chunk to table
                    self.graph_db.create_relationship(
                        'Table', {'id': table_id},
                        'HAS_CONTENT', {},
                        'Chunk', {'id': chunk_id}
                    )
                    
                    # Connect document to table
                    self.graph_db.create_relationship(
                        'Document', {'id': document_id},
                        'HAS_TABLE', {},
                        'Table', {'id': table_id}
                    )
            
            elif chunk_type == 'image_text':
                image_index = chunk.get('metadata', {}).get('image_index')
                if image_index is not None:
                    # Create image node
                    image_id = f"{document_id}_image_{image_index}"
                    self.graph_db.create_node('Image', {
                        'id': image_id,
                        'index': image_index,
                        'page': chunk.get('metadata', {}).get('page')
                    })
                    
                    # Connect chunk to image
                    self.graph_db.create_relationship(
                        'Image', {'id': image_id},
                        'HAS_TEXT', {},
                        'Chunk', {'id': chunk_id}
                    )
                    
                    # Connect document to image
                    self.graph_db.create_relationship(
                        'Document', {'id': document_id},
                        'HAS_IMAGE', {},
                        'Image', {'id': image_id}
                    )
    
    def store_in_vector_db(self, document_id: str, metadata: Dict[str, Any],
                          chunks: List[Dict[str, Any]], **kwargs) -> None:
        """
        Store PDF document in vector database.
        
        Args:
            document_id: Document ID
            metadata: Document metadata
            chunks: Document chunks
            **kwargs: Additional storage options
        """
        # Add PDF-specific metadata
        metadata['content_type'] = 'application/pdf'
        
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