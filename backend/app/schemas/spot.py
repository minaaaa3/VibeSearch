from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from uuid import UUID

class SpotBase(BaseModel):
    name: str
    address: Optional[str] = None
    vibe_summary: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)

class SpotResponse(SpotBase):
    id: UUID
    latitude: float
    longitude: float

    class Config:
        from_attributes = True

class FeedbackCreate(BaseModel):
    session_id: UUID
    spot_id: UUID
    user_rating: str
    comment: Optional[str] = None
