from pydantic import BaseModel
from typing import List, Optional

class ChatRequest(BaseModel):
    message: str
    thread_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    thread_id: str
    context: Optional[str] = None
    requires_approval: bool = False

class ApproveRequest(BaseModel):
    thread_id: str
