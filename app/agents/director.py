import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from app.agents.prompts import DIRECTOR_SYSTEM_PROMPT

load_dotenv()

llm_director = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.2 
)

director_prompt = ChatPromptTemplate.from_messages([
    ("system", DIRECTOR_SYSTEM_PROMPT),
    ("human", "Recent chat history: {chat_history}")
])

director_chain = director_prompt | llm_director