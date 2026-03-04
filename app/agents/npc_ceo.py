import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from app.agents.prompts import CEO_SYSTEM_PROMPT
from app.services.rag_pipeline import tools
from dotenv import load_dotenv

load_dotenv()

llm_ceo = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.5
)

llm_ceo_with_tools = llm_ceo.bind_tools(tools)

ceo_prompt = ChatPromptTemplate.from_messages([
    ("system", CEO_SYSTEM_PROMPT),
    MessagesPlaceholder(variable_name="messages")
])

ceo_chain = ceo_prompt | llm_ceo_with_tools