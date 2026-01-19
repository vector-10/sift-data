from pydantic import BaseModel
from typing import Optional, Dict, Any

class DocumentBase(BaseModel):
    filename: str

class DocumentCreate(DocumentBase):
    file_path: str
    owner_id: int

class DocumentUpdate(BaseModel):
    status: Optional[str] = None
    extracted_text: Optional[str] = None
    structured_data: Optional[Dict[str, Any]] = None

class DocumentRead(DocumentBase):
    id: int
    status: str
    extracted_text: Optional[str] = None
    structured_data: Optional[Dict[str, Any]] = None
    owner_id: int

    class Config:
        from_attributes = True