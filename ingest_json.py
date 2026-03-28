import os
import shutil
from datasets import load_dataset
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

print("🚀 Initiating Phase 1: Massive JSON Dataset Ingestion...")

# 1. Nuke the old database to prevent contamination
db_path = "./chroma_db"
if os.path.exists(db_path):
    print("🗑️ Deleting old database...")
    shutil.rmtree(db_path)

# 2. Download the JSON dataset from Hugging Face
print("⬇️ Downloading scheme data from Hugging Face (shrijayan/gov_myscheme)...")
try:
    # This pulls the dataset directly into memory
    dataset = load_dataset("shrijayan/gov_myscheme", split="train")
    print(f"📦 Successfully loaded {len(dataset)} schemes!")
except Exception as e:
    print(f"❌ Failed to load dataset: {e}")
    exit()

# 3. Format the JSON data into LangChain Documents
documents = []
for item in dataset:
    # We structure the text so the AI knows exactly what it's reading
    scheme_name = item.get('scheme_name', 'Unnamed Scheme')
    details = item.get('details', 'No details provided.')
    benefits = item.get('benefits', 'No benefits listed.')
    
    content = f"**{scheme_name}**\n\nDETAILS: {details}\n\nBENEFITS: {benefits}"
    
    # We store metadata so we can filter by state/ministry later if needed
    metadata = {
        "scheme_name": scheme_name,
        "source": "hf_json_database"
    }
    
    documents.append(Document(page_content=content, metadata=metadata))

# 4. Inject into ChromaDB
print("🧠 Embedding 2,000+ schemes into local Vector Store... (This may take a minute)")
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = Chroma.from_documents(documents, embeddings, persist_directory=db_path)

print("✅ SUCCESS! Your offline brain now contains thousands of real government schemes.")