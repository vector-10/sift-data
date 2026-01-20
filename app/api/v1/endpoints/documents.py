from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from pathlib import Path
import shutil
from datetime import datetime

from app.api.deps import get_current_user, get_db
from app.models.user import User
from app.models.document import Document
from app.schemas.document import UploadResponse, DocumentRead, SearchResponse
from app.services.background import process_document_task

router = APIRouter()


UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@router.post("/upload", response_model= UploadResponse)
async def upload_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    allowed_types = ["application/pdf", "image/jpeg", "image/png"]
    if file.content_type not in allowed_types:
        raise HTTPException(400, "Only PDF and images allowed")
    
    # Save file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}_{file.filename}"
    file_path = UPLOAD_DIR / filename
    
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Save to DB
    doc = Document(
        filename=filename,
        file_path=str(file_path),
        user_id=current_user.id,
        status="uploaded"
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)

    # add background task
    background_tasks.add_task(process_document_task, doc.id)
    
    return {"id": doc.id, "filename": filename, "status": "processing"}


@router.get("/", response_model=list[DocumentRead])
async def list_documents(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all documents for current user"""
    docs = db.query(Document).filter(
        Document.user_id == current_user.id
    ).all()
    
    return [{
        "id": doc.id,
        "filename": doc.filename,
        "status": doc.status,
        "parsed_data": doc.parsed_data
    } for doc in docs]



@router.get("/{document_id}/status", response_model=DocumentRead)
async def get_document_status(
        document_id: int,
         current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    doc = db.query(Document).filter(
        Document.id == document_id,
        Document.user_id == current_user.id
    ).first()
    
    if not doc:
        raise HTTPException(404, "Document not found")
    
    return {
        "id": doc.id,
        "filename": doc.filename,
        "status": doc.status,
        "parsed_data": doc.parsed_data,
        "error": doc.error_message,
        "user_id": doc.user_id
    }



@router.get("/search", response_model=SearchResponse)
async def search_documents(
    q: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Search documents by vendor, invoice number, or extracted text"""
    
    # Search in extracted_text and parsed_data
    documents = db.query(Document).filter(
        Document.user_id == current_user.id,
        Document.status == "completed"
    ).all()
    
    results = []
    search_term = q.lower()
    
    for doc in documents:
        # Search in extracted text
        if doc.extracted_text and search_term in doc.extracted_text.lower():
            results.append({
                "id": doc.id,
                "filename": doc.filename,
                "parsed_data": doc.parsed_data,
                "match_type": "text"
            })
            continue
        
        # Search in parsed data (vendor, invoice_number)
        if doc.parsed_data:
            parsed = doc.parsed_data
            if (parsed.get("vendor") and search_term in parsed.get("vendor", "").lower()) or \
               (parsed.get("invoice_number") and search_term in str(parsed.get("invoice_number", "")).lower()):
                results.append({
                    "id": doc.id,
                    "filename": doc.filename,
                    "parsed_data": doc.parsed_data,
                    "match_type": "metadata"
                })
    
    return {"query": q, "count": len(results), "results": results}

