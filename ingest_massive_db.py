import os
import shutil
from datasets import load_dataset
from tqdm import tqdm
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter

print("🚀 Initiating Production-Grade Database Ingestion...")

# 1. Clear the old database safely
db_path = "./chroma_db"
if os.path.exists(db_path):
    print("🗑️ Clearing old database...")
    shutil.rmtree(db_path)

# 2. Download the massive dataset
print("⬇️ Downloading PDF dataset from Hugging Face...")
dataset = load_dataset("shrijayan/gov_myscheme", split="train")
print(f"📦 Successfully loaded {len(dataset)} government PDFs!")

# 3. Setup the Text Splitter (Crucial for RAG)
# We break PDFs into 1000-character chunks with 200-character overlap
# so the AI doesn't miss context that crosses between two chunks.
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    length_function=len,
)

documents = []

print("⚙️ Extracting and chunking text from PDFs... (This will take a while)")
# We use tqdm to create a progress bar in the terminal
for i, item in enumerate(tqdm(dataset, desc="Processing PDFs")):
    try:
        # pdfplumber extracts the text into a dictionary structure via the datasets library
        extracted_data = item.get('pdf', {})
        raw_text = extracted_data.get('text', '')
        
        if not raw_text.strip():
            continue # Skip empty PDFs
            
        # Get metadata if available, otherwise use a generic name
        file_name = item.get('file_name', f'Scheme_Document_{i}')
        
        # Split the massive text into smaller chunks
        chunks = text_splitter.split_text(raw_text)
        
        for chunk_num, chunk in enumerate(chunks):
            documents.append(
                Document(
                    page_content=chunk, 
                    metadata={"source": file_name, "chunk": chunk_num}
                )
            )
    except Exception as e:
        # If one PDF is corrupted, we skip it and keep going. Never crash the pipeline!
        continue

print(f"\n✂️ Sliced 700+ PDFs into {len(documents)} searchable text chunks.")

# 4. Inject into ChromaDB
print("🧠 Embedding chunks into Vector Store... (CPU is working hard now)")
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = Chroma.from_documents(documents, embeddings, persist_directory=db_path)

print("✅ MASSIVE INGESTION COMPLETE! Your offline brain is now a powerhouse.")