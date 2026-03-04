import os
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader, Docx2txtLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

DATA_PATH = "./data/knowledge_base"
FAISS_PATH = "./data/faiss_index"

def create_db():
    loaders = {
        ".pdf": DirectoryLoader(DATA_PATH, glob="**/*.pdf", loader_cls=PyPDFLoader),
        ".docx": DirectoryLoader(DATA_PATH, glob="**/*.docx", loader_cls=Docx2txtLoader),
        ".md": DirectoryLoader(DATA_PATH, glob="**/*.md", loader_cls=TextLoader)
    }
    
    documents = []
    for ext, loader in loaders.items():
        try:
            documents.extend(loader.load())
        except Exception as e:
            print(f"Skip {ext} error: {e}")

    if not documents:
        return

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = text_splitter.split_documents(documents)

    for chunk in chunks:
        chunk.page_content = f"passage: {chunk.page_content}"

    embeddings = HuggingFaceEmbeddings(model_name="intfloat/e5-base-v2")
    vector_db = FAISS.from_documents(chunks, embeddings)
    vector_db.save_local(FAISS_PATH)
    print("Done")

if __name__ == "__main__":
    create_db()