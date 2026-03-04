import os
import json
from fastapi import APIRouter
from pydantic import BaseModel
from langchain_core.messages import HumanMessage, messages_from_dict, messages_to_dict
from app.services.engine import ai_engine

router = APIRouter()

HISTORY_FILE = "data/chat_history.json"

os.makedirs("data", exist_ok=True)

def load_history():
    if not os.path.exists(HISTORY_FILE):
        return {}
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            history = {}
            for session_id, session_data in data.items():
                history[session_id] = {
                    "messages": messages_from_dict(session_data.get("messages", [])),
                    "sentiment_score": session_data.get("sentiment_score", 5) 
                }
            return history
    except Exception:
        return {}

def save_history(memory_dict):
    data_to_save = {}
    for session_id, session_data in memory_dict.items():
        data_to_save[session_id] = {
            "messages": messages_to_dict(session_data["messages"]),
            "sentiment_score": session_data["sentiment_score"]
        }
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data_to_save, f, ensure_ascii=False, indent=4)

class ChatRequest(BaseModel):
    session_id: str
    user_message: str

@router.post("/chat")
async def chat_endpoint(request: ChatRequest):
    session_id = request.session_id or str(uuid.uuid4())
    chat_memory = load_history()
    
    if session_id not in chat_memory:
        chat_memory[session_id] = {"messages": [], "sentiment_score": 5}
        
    messages = chat_memory[session_id]["messages"]
    current_score = chat_memory[session_id]["sentiment_score"]
    
    messages.append(HumanMessage(content=request.user_message))
    
    state = {"messages": messages, "sentiment_score": current_score}
    result = ai_engine.invoke(state)
    
    chat_memory[session_id]["messages"] = result["messages"]
    chat_memory[session_id]["sentiment_score"] = result["sentiment_score"]
    save_history(chat_memory)
    
    raw_content = result["messages"][-1].content
    
    if isinstance(raw_content, list):
        ai_response = "".join([item.get("text", "") for item in raw_content if isinstance(item, dict) and "text" in item])
    else:
        ai_response = str(raw_content)
    
    return {
        "session_id": session_id,
        "npc_response": ai_response,
        "debug_director_hint": result.get("director_hint", ""),
        "sentiment_score": result["sentiment_score"],
    }