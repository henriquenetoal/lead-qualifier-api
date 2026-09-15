from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class LeadCreate(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    status: str = "novo"
    notes: Optional[str] = None

class LeadResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: Optional[str] = None
    status: str
    notes: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True