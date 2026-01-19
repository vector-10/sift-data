from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship
from app.models.base import Base

class user(Base):
    __tablename__ = "users"

    id = Column(Integer, Primary_key=True, index=True)
    email(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

    documents = relationship("Document", back_populates="owner")