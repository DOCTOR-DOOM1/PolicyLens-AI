import os
import streamlit as st

st.set_page_config(page_title="PolicyLens AI", page_icon="🏛️", layout="wide", initial_sidebar_state="expanded")

# --- Download chroma_db from HF Dataset at startup if not present ---
if not os.path.exists("chroma_db/chroma.sqlite3"):
    from huggingface_hub import snapshot_download
    st.info("Downloading vector database (first boot, ~250MB)... Please wait.")
    hf_token = os.getenv("HF_TOKEN")
    try:
        if "HF_TOKEN" in st.secrets:
            hf_token = st.secrets["HF_TOKEN"]
    except Exception:
        pass

    if not hf_token:
        st.error("🚨 HF_TOKEN is missing! Please add it to your Streamlit Cloud Secrets to bypass the Rate Limit. Go to Manage App -> Settings -> Secrets and paste your .env contents.")
        st.stop()

    snapshot_download(
        repo_id="Doctor-Doom2/policylens-chromadb",
        repo_type="dataset",
        local_dir="chroma_db",
        local_dir_use_symlinks=False,
        token=hf_token
    )

# Run the main app
with open("policylens_ui.py", encoding="utf-8") as f:
    exec(f.read())