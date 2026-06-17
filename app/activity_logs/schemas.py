# app/activity_logs/schemas.py

from pydantic import BaseModel
from typing import Optional

class ActivityLogBase(BaseModel):
    user_id: Optional[int] = None
    entity_type: Optional[str] = None
    entity_id: Optional[str] = None
    action: Optional[str] = None
    method: Optional[str] = None
    path: Optional[str] = None
    status_code: Optional[int] = None
