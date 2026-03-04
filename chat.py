import requests
import uuid
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000/api/v1/chat"

def generate_session_id():
    return f"live_interview_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:6]}"

def start_chat():
    session_id = "live_interview_001"
    
    print("="*60)
    print("STARTING SIMULATION: INTERVIEW WITH GUCCI CEO")
    print("Tip: Try asking follow-up questions to test context memory.")
    print("Type 'new session' to start a fresh conversation.")
    print("Type 'quit' or 'exit' to stop.")
    print(f"Current Session: {session_id}")
    print("="*60 + "\n")

    while True:
        user_input = input("You (OD Director): ")
        
        if user_input.lower() in ['quit', 'exit']:
            print("Simulation ended.")
            break

        if user_input.lower() in ['new session', 'new_session', '/new']:
            session_id = generate_session_id()
            print(f"\n New session started: {session_id}")
            print("Context has been reset. Starting fresh conversation.\n")
            continue
            
        if not user_input.strip():
            continue
            
        payload = {
            "session_id": session_id,
            "user_message": user_input
        }
        
        try:
            response = requests.post(BASE_URL, json=payload)
            if response.status_code == 200:
                data = response.json()
                
                if data.get('debug_director_hint'):
                    print(f"   [Director Hint: {data['debug_director_hint']}]")
                    
                print(f"CEO: {data['npc_response']}\n")
            else:
                print(f"Server Error: {response.text}")
        except Exception as e:
            print(f"Connection Error: {e}")

if __name__ == "__main__":
    start_chat()