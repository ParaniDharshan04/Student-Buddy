import PyPDF2
import docx
import io
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class FileService:
    """Service for handling file uploads and text extraction"""
    
    SUPPORTED_EXTENSIONS = {'.pdf', '.txt', '.docx', '.doc'}
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    
    def extract_text_from_file(self, file_content: bytes, filename: str) -> str:
        """
        Extract text content from uploaded file
        
        Args:
            file_content: File content as bytes
            filename: Original filename
            
        Returns:
            Extracted text content
        """
        try:
            extension = self._get_file_extension(filename)
            
            if extension == '.pdf':
                return self._extract_from_pdf(file_content)
            elif extension == '.txt':
                return self._extract_from_txt(file_content)
            elif extension in ['.docx', '.doc']:
                return self._extract_from_docx(file_content)
            else:
                raise ValueError(f"Unsupported file type: {extension}")
                
        except Exception as e:
            logger.error(f"Error extracting text from file: {str(e)}")
            raise Exception(f"Failed to extract text from file: {str(e)}")
    
    def _get_file_extension(self, filename: str) -> str:
        """Get file extension in lowercase"""
        return '.' + filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''
    
    def _extract_from_pdf(self, file_content: bytes) -> str:
        """Extract text from PDF file"""
        try:
            pdf_file = io.BytesIO(file_content)
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            text_content = []
            for page in pdf_reader.pages:
                text = page.extract_text()
                if text:
                    text_content.append(text)
            
            return '\n\n'.join(text_content)
            
        except Exception as e:
            raise Exception(f"Failed to extract text from PDF: {str(e)}")
    
    def _extract_from_txt(self, file_content: bytes) -> str:
        """Extract text from TXT file"""
        try:
            # Try different encodings
            for encoding in ['utf-8', 'latin-1', 'cp1252']:
                try:
                    return file_content.decode(encoding)
                except UnicodeDecodeError:
                    continue
            
            raise Exception("Could not decode text file with supported encodings")
            
        except Exception as e:
            raise Exception(f"Failed to extract text from TXT: {str(e)}")
    
    def _extract_from_docx(self, file_content: bytes) -> str:
        """Extract text from DOCX file"""
        try:
            doc_file = io.BytesIO(file_content)
            doc = docx.Document(doc_file)
            
            text_content = []
            for paragraph in doc.paragraphs:
                if paragraph.text.strip():
                    text_content.append(paragraph.text)
            
            return '\n\n'.join(text_content)
            
        except Exception as e:
            raise Exception(f"Failed to extract text from DOCX: {str(e)}")
    
    def validate_file(self, filename: str, file_size: int) -> Dict[str, Any]:
        """
        Validate uploaded file
        
        Args:
            filename: Original filename
            file_size: File size in bytes
            
        Returns:
            Validation result dictionary
        """
        errors = []
        
        # Check file extension
        extension = self._get_file_extension(filename)
        if extension not in self.SUPPORTED_EXTENSIONS:
            errors.append(f"Unsupported file type. Supported types: {', '.join(self.SUPPORTED_EXTENSIONS)}")
        
        # Check file size
        if file_size > self.MAX_FILE_SIZE:
            errors.append(f"File too large. Maximum size: {self.MAX_FILE_SIZE / (1024*1024)}MB")
        
        if file_size == 0:
            errors.append("File is empty")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "extension": extension,
            "size": file_size
        }
