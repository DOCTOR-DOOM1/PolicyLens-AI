import os
import streamlit as st

# --- Download chroma_db from HF Dataset at startup if not present ---
if not os.path.exists("chroma_db/chroma.sqlite3"):
    from huggingface_hub import snapshot_download
    st.info("Downloading vector database (first boot, ~250MB)... Please wait.")
    snapshot_download(
        repo_id="Doctor-Doom2/policylens-chromadb",
        repo_type="dataset",
        local_dir="chroma_db",
        local_dir_use_symlinks=False,
    )
    st.rerun()

# Run the main app
with open("policylens_ui.py", encoding="utf-8") as f:
    exec(f.read())