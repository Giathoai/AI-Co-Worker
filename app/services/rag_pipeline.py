import os
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.tools import tool

FAISS_PATH = "./data/faiss_index"
embeddings = HuggingFaceEmbeddings(model_name="intfloat/e5-base-v2")

if os.path.exists(FAISS_PATH):
    vector_db = FAISS.load_local(FAISS_PATH, embeddings, allow_dangerous_deserialization=True)
    retriever = vector_db.as_retriever(search_kwargs={"k": 3})
else:
    print("Not Found FAISS index")
    retriever = None

@tool
def search_gucci_guidelines(query: str) -> str:
    """Search Doc"""
    if not retriever:
        return "Error data"
        
    docs = retriever.invoke(f"query: {query}")
    return "\n\n".join([doc.page_content.replace("passage: ", "") for doc in docs])

tools = [search_gucci_guidelines]