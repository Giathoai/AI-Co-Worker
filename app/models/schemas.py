from pydantic import BaseModel, Field
from typing import Optional

class ChatRequest(BaseModel):
    session_id: str = Field(..., description="ID for a session")
    user_message: str = Field(..., description="Content of the message the user sends to the AI Co-Worker")

class ChatResponse(BaseModel):
    session_id: str
    npc_name: str = "Gucci Group CEO"
    npc_response: str
    debug_director_hint: Optional[str] = Field(None, description="Director 's hint")