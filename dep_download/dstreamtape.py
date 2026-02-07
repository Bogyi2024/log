import requests
import time
import os
import sys
import subprocess
from huggingface_hub import HfApi

# --- CONFIGURATION ---
LOGIN = os.environ.get("ST_LOGIN")
KEY = os.environ.get("ST_KEY")
HF_TOKEN = os.environ.get("HF_TOKEN")
REPO_ID = os.environ.get("HF_REPO_ID")
REPO_TYPE = os.environ.get("HF_REPO_TYPE", "model")
LINKS_RAW = os.environ.get("ST_LINKS", "")
LINKS = [l.strip() for l in LINKS_RAW.splitlines() if l.strip()]

def extract_file_id(url):
    if "/v/" in url: return url.split("/v/")[1].split("/")[0]
    if "/e/" in url: return url.split("/e/")[1].split("/")[0]
    return url

def process_file(file_id):
    print(f"\n🚀 Processing: {file_id}")
    
    # Step 1: Get Ticket
    res = requests.get(f"https://api.streamtape.com/file/dlticket?file={file_id}&login={LOGIN}&key={KEY}").json()
    if res['status'] != 200:
        print(f"❌ Ticket Error: {res.get('msg')}")
        return

    ticket = res['result']['ticket']
    time.sleep(res['result']['wait_time'])

    # Step 2: Get Final Link
    dl_res = requests.get(f"https://api.streamtape.com/file/dl?file={file_id}&ticket={ticket}").json()
    if dl_res['status'] != 200:
        print(f"❌ DL URL Error: {dl_res.get('msg')}")
        return

    final_url = dl_res['result']['url']
    filename = dl_res['result']['name']
    
    # Step 3: Download using aria2c (16 connections for speed)
    print(f"⬇️ Downloading with aria2: {filename}")
    cmd = ["aria2c", "-x", "16", "-s", "16", "-o", filename, final_url]
    subprocess.run(cmd, check=True)

    # Step 4: Upload to HF
    print(f"⬆️ Uploading to HF {REPO_TYPE}: {REPO_ID}")
    api = HfApi(token=HF_TOKEN)
    api.upload_file(path_or_fileobj=filename, path_in_repo=filename, repo_id=REPO_ID, repo_type=REPO_TYPE)
    
    # Step 5: Delete local file
    os.remove(filename)
    print(f"✅ Finished and Cleaned: {filename}")

if __name__ == "__main__":
    if not LOGIN or not KEY:
        print("❌ Error: Credentials missing.")
        sys.exit(1)
        
    for link in LINKS:
        try:
            process_file(extract_file_id(link))
        except Exception as e:
            print(f"❌ Failed {link}: {e}")
