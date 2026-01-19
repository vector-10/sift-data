import asyncio
from sqlalchemy.orm import Session
from pathlib import Path

from app.db.session import SessionLocal
from app.models.document import Document
from app.services.extractor import extract_text
from app.services.parser import parse_invoice


async def process_document_task(document_id: int):
    """Background task to extract and parse document"""
    db = SessionLocal()
    
    try:

        doc = db.query(Document).filter(Document.id == document_id).first()
        if not doc:
            return
        
        doc.status = "processing"
        db.commit()
        
        raw_text = extract_text(doc.file_path)
        
        parsed_data = parse_invoice(raw_text)
        
        doc.extracted_text = raw_text
        doc.parsed_data = parsed_data  
        doc.status = "completed"
        db.commit()
        
    except Exception as e:
        doc.status = "failed"
        doc.error_message = str(e)
        db.commit()
    
    finally:
        db.close()