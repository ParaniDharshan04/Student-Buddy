from fastapi import APIRouter, UploadFile, File, HTTPException, status
from app.services.file_service import FileService
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["upload"])

file_service = FileService()

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    Upload a file and extract text content
    
    - **file**: PDF, TXT, or DOCX file containing study materials
    
    Returns extracted text content
    """
    try:
        # Read file content
        file_content = await file.read()
        
        # Validate file
        validation = file_service.validate_file(file.filename, len(file_content))
        if not validation["valid"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"errors": validation["errors"]}
            )
        
        # Extract text
        logger.info(f"Extracting text from file: {file.filename}")
        extracted_text = file_service.extract_text_from_file(file_content, file.filename)
        
        if not extracted_text or len(extracted_text.strip()) < 10:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Could not extract meaningful text from the file"
            )
        
        # Limit content length to avoid API quota issues
        max_length = 15000  # ~3000 words
        if len(extracted_text) > max_length:
            logger.warning(f"Content too long ({len(extracted_text)} chars), truncating to {max_length}")
            extracted_text = extracted_text[:max_length] + "\n\n[Content truncated due to length...]"
        
        return {
            "filename": file.filename,
            "content": extracted_text,
            "length": len(extracted_text),
            "word_count": len(extracted_text.split())
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing file upload: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process file: {str(e)}"
        )

@router.get("/upload/supported-formats")
async def get_supported_formats():
    """Get list of supported file formats"""
    return {
        "formats": [
            {
                "extension": ".pdf",
                "name": "PDF Document",
                "description": "Portable Document Format"
            },
            {
                "extension": ".txt",
                "name": "Text File",
                "description": "Plain text document"
            },
            {
                "extension": ".docx",
                "name": "Word Document",
                "description": "Microsoft Word document"
            }
        ],
        "max_file_size_mb": 10
    }
