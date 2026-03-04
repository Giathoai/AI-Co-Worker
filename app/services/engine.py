import os
import re
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, ToolMessage
from langchain_core.prompts import ChatPromptTemplate
from app.agents.prompts import CEO_SYSTEM_PROMPT, DIRECTOR_SYSTEM_PROMPT
from app.services.rag_pipeline import search_gucci_guidelines
from app.services.sim_tools import (
    kpi_calculator, 
    hr_ab_simulator, 
    get_safety_disclaimer, 
    export_portfolio_pack
)

load_dotenv()

sim_tools = [
    kpi_calculator,
    hr_ab_simulator,
    get_safety_disclaimer,
    export_portfolio_pack
]

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.2)
all_tools = [search_gucci_guidelines] + sim_tools
llm_with_tools = llm.bind_tools(all_tools)

director_prompt = ChatPromptTemplate.from_messages([
    ("system", DIRECTOR_SYSTEM_PROMPT),
    ("human", "{chat_history}")
])
director_chain = director_prompt | llm

class AIEngine:
    def invoke(self, state: dict):
        messages = state.get("messages", [])
        sentiment_score = state.get("sentiment_score", 5) 
        
        chat_history_text = "\n".join([f"{m.type}: {m.content}" for m in messages[-3:]])
        
        try:
            hint = director_chain.invoke({"chat_history": chat_history_text}).content.strip()
            if hint.upper() in ["NONE", "NONE.", ""]:
                hint = ""
        except:
            hint = ""

        ceo_messages = list(messages)
        
        if not any(isinstance(m, SystemMessage) and "CEO of Gucci Group" in m.content for m in ceo_messages):
            ceo_messages.insert(0, SystemMessage(content=CEO_SYSTEM_PROMPT))
        
        system_content = f"[SYSTEM UPDATE] Your current sentiment score towards the user is {sentiment_score}/10. Update it based on their message and start your reply with [SENTIMENT: X]."
        if hint:
            system_content += f"\n[DIRECTOR HINT]: {hint}"
            
        system_update_msg = SystemMessage(content=system_content)
        ceo_messages.insert(-1, system_update_msg)
        
        while True:
            response = llm_with_tools.invoke(ceo_messages)
            ceo_messages.append(response)
            
            if not response.tool_calls:
                break
                
            for tool_call in response.tool_calls:
                tool_fn = next((t for t in all_tools if t.name == tool_call["name"]), None)
                if tool_fn:
                    try:
                        tool_result = tool_fn.invoke(tool_call["args"])
                    except Exception as e:
                        tool_result = f"Error: {e}"
                else:
                    tool_result = f"Error: Tool {tool_call['name']} not found."
                    
                ceo_messages.append(ToolMessage(
                    content=str(tool_result),
                    tool_call_id=tool_call["id"],
                    name=tool_call["name"]
                ))
        
        final_ai_msg = ceo_messages[-1]
        
        def extract_and_clean(text_content):
            match = re.search(r'\[SENTIMENT:\s*(\d+)\]', text_content)
            if match:
                new_score = max(1, min(10, int(match.group(1))))
                clean_text = re.sub(r'\[SENTIMENT:\s*\d+\]', '', text_content).strip()
                return new_score, clean_text
            return None, text_content

        if isinstance(final_ai_msg.content, str):
            new_score, clean_text = extract_and_clean(final_ai_msg.content)
            if new_score is not None:
                sentiment_score = new_score
            final_ai_msg.content = clean_text
            
        elif isinstance(final_ai_msg.content, list):
            for item in final_ai_msg.content:
                if isinstance(item, dict) and "text" in item:
                    new_score, clean_text = extract_and_clean(item["text"])
                    if new_score is not None:
                        sentiment_score = new_score
                    item["text"] = clean_text

        cleaned_messages = [m for m in ceo_messages if m != system_update_msg]

        return {
            "messages": cleaned_messages,
            "director_hint": hint,
            "sentiment_score": sentiment_score
        }

ai_engine = AIEngine()