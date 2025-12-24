import os
from typing import Optional
from fastapi import UploadFile, HTTPException
import PyPDF2
from docx import Document
from ..config import settings


class FileService:
    @staticmethod
    def validate_file(file: UploadFile) -> None:
        """Validate uploaded file"""
        # Check file extension
        file_ext = os.path.splitext(file.filename)[1].lower()
        if file_ext not in settings.allowed_extensions_list:
            raise HTTPException(
                status_code=400,
                detail=f"File type not allowed. Allowed types: {', '.join(settings.allowed_extensions_list)}"
            )
    
    @staticmethod
    async def extract_text_from_file(file: UploadFile) -> str:
        """Extract text from uploaded file"""
        FileService.validate_file(file)
        
        file_ext = os.path.splitext(file.filename)[1].lower()
        content = await file.read()
        
        try:
            if file_ext == '.pdf':
                return FileService._extract_from_pdf(content)
            elif file_ext == '.docx':
                return FileService._extract_from_docx(content)
            elif file_ext == '.txt':
                return content.decode('utf-8')
            else:
                raise HTTPException(status_code=400, detail="Unsupported file type")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error extracting text: {str(e)}")
    
    @staticmethod
    def _extract_from_pdf(content: bytes) -> str:
        """Extract text from PDF"""
        import io
        pdf_file = io.BytesIO(content)
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        
        if not text.strip():
            raise HTTPException(status_code=400, detail="No text found in PDF")
        
        return text.strip()
    
    @staticmethod
    def _extract_from_docx(content: bytes) -> str:
        """Extract text from DOCX"""
        import io
        docx_file = io.BytesIO(content)
        doc = Document(docx_file)
        
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        
        if not text.strip():
            raise HTTPException(status_code=400, detail="No text found in DOCX")
        
        return text.strip()
    
    @staticmethod
    def chunk_text(text: str, max_chunk_size: int = 4000) -> list[str]:
        """Split long text into chunks for processing"""
        if len(text) <= max_chunk_size:
            return [text]
        
        chunks = []
        words = text.split()
        current_chunk = []
        current_size = 0
        
        for word in words:
            word_size = len(word) + 1
            if current_size + word_size > max_chunk_size:
                chunks.append(' '.join(current_chunk))
                current_chunk = [word]
                current_size = word_size
            else:
                current_chunk.append(word)
                current_size += word_size
        
        if current_chunk:
            chunks.append(' '.join(current_chunk))
        
        return chunks


file_service = FileService()
