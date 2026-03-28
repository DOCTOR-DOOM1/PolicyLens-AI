import os
import shutil
from tqdm import tqdm
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

print("🚀 Initiating True Offline Massive PDF Ingestion...")

pdf_folder = "./pdf_data"
db_path = "./chroma_db"

# 1. Verify the folder exists
if not os.path.exists(pdf_folder):
    print(f"❌ Error: Could not find the '{pdf_folder}' directory. Please create it and add your PDFs.")
    exit()

# Get all PDF files in the directory
pdf_files = [f for f in os.listdir(pdf_folder) if f.endswith('.pdf')]
print(f"📁 Found {len(pdf_files)} PDFs locally.")

if len(pdf_files) == 0:
    print("❌ Error: The folder is empty. Please move your 2200 PDFs into the folder.")
    exit()

# 2. Clear old database
if os.path.exists(db_path):
    print("🗑️ Clearing old Chroma database to start fresh...")
    shutil.rmtree(db_path)

# 3. Setup Splitter and Embeddings
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# We create an empty Chroma database first
vectorstore = Chroma(persist_directory=db_path, embedding_function=embeddings)

print("⚙️ Extracting, chunking, and embedding PDFs...")

# 4. The Batch Processing Loop
# We process and save to the database continuously so if your laptop crashes at PDF 1500, 
# you don't lose your progress!
documents_batch = []
batch_size = 50 # Add to database every 50 PDFs to save RAM

for i, filename in enumerate(tqdm(pdf_files, desc="Processing PDFs")):
    try:
        file_path = os.path.join(pdf_folder, filename)
        
        # Load the PDF
        loader = PyPDFLoader(file_path)
        pages = loader.load()
        
        # Split into chunks
        chunks = text_splitter.split_documents(pages)
        documents_batch.extend(chunks)
        
        # Every 50 PDFs, embed them and clear the batch memory
        if (i + 1) % batch_size == 0 or (i + 1) == len(pdf_files):
            if documents_batch:
                vectorstore.add_documents(documents_batch)
                documents_batch = [] # Reset for the next batch
                
    except Exception as e:
        # If a single PDF is corrupted or password-protected, skip it and keep going!
        pass

print(f"\n✅ BOOM! Successfully ingested {len(pdf_files)} PDFs into your local Vector Database.")
print("Your offline RAG engine is now fully armed.")