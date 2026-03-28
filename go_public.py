import os
import sys
import subprocess
import time
import re
import threading

def run_public():
    print("==========================================================")
    print(" STARTING POLICY-LENS LOCALLY AND MAKING IT PUBLIC ")
    print("==========================================================")
    print("\n1. Starting Streamlit application on port 8501...")
    
    # Start Streamlit
    streamlit_proc = subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run", "app.py", "--server.port=8501", "--server.headless=true"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    
    time.sleep(4) # Give Streamlit a moment to spin up
    print("   [OK] Streamlit is running internally.")
    
    print("\n2. Establishing secure public tunnel via localhost.run...")
    
    # Start SSH tunnel
    ssh_proc = subprocess.Popen(
        ["ssh", "-o", "StrictHostKeyChecking=no", "-R", "80:localhost:8501", "nokey@localhost.run", "-T", "-n"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )
    
    public_url = None
    
    # Read SSH output to find the URL
    for line in ssh_proc.stdout:
        line = line.strip()
        if "tunneled with tls termination" in line or "https://" in line:
            match = re.search(r'(https://[a-zA-Z0-9.-]+\.lhr\.life)', line)
            if match:
                public_url = match.group(1)
                break
                
    if public_url:
        print("\n==========================================================")
        print(f" SUCCESS! YOUR PUBLIC URL IS READY ")
        print("==========================================================")
        print(f"--> {public_url} <--")
        print("\nSend this link to your judges/team. It is live RIGHT NOW!")
        print("Press Ctrl+C in this terminal to shut it down.")
        
        try:
            # Keep alive
            ssh_proc.wait()
        except KeyboardInterrupt:
            pass
    else:
        print("\n Failed to establish public tunnel. Please check your internet connection.")
        
    # Cleanup
    print("\nShutting down...")
    ssh_proc.terminate()
    streamlit_proc.terminate()
    sys.exit(0)

if __name__ == "__main__":
    run_public()
