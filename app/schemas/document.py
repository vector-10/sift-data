from pydantic import BaseModel
from typing import Optional, Dict, Any

class DocumentBase(BaseModel):
    filename: str

class DocumentCreate(DocumentBase):
    file_path: str
    user_id: int

class DocumentUpdate(BaseModel):
    status: Optional[str] = None
    extracted_text: Optional[str] = None
    parsed_data: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None

class DocumentRead(DocumentBase):
    id: int
    status: str
    extracted_text: Optional[str] = None
    parsed_data: Optional[Dict[str, Any]] = None  
    error_message: Optional[str] = None  
    user_id: int

    class Config:
        from_attributes = True

class UploadResponse(BaseModel):
    id: int
    filename: str
    status: str


class SearchResponse(BaseModel):
    query: str
    count: int
    results: list 