import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

load_dotenv()

print("🚀 Starting Phase 1: Building the AI Brain...")

# 1. Load the PDFs from your data folder
print("📄 Loading PDFs from ./data...")
loader = PyPDFDirectoryLoader("./data")
documents = loader.load()
print(f"✅ Loaded {len(documents)} document pages.")

# 2. Chop the text into small, readable chunks
print("✂️ Chunking text...")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = text_splitter.split_documents(documents)
print(f"✅ Split into {len(chunks)} chunks.")

# 3. Generate embeddings LOCALLY (Bypassing all API limits)
print("🧠 Generating embeddings offline using your CPU...")
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# 4. Save to ChromaDB
vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="./chroma_db"
)

print("🎉 SUCCESS! Your local vector database is built and ready.")