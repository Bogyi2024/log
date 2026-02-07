import requests
import time
import os
import subprocess
from huggingface_hub import HfApi

# Load Vars from YAML Env block
LOGIN = os.environ.get("ST_LOGIN")
KEY = os.environ.get("ST_KEY")
LINKS_RAW = os.environ.get("ST_LINKS", "")
REPO_ID = os.environ.get("HF_REPO_ID")
REPO_TYPE = os.environ.get("HF_REPO_TYPE", "model")
HF_TOKEN = os.environ.get("HF_TOKEN")

def process_file(url):
    file_id = url.split("/v/")[1].split("/")[0] if "/v/" in url else url.strip()
    
    # 1. Get Ticket
    res = requests.get(f"https://api.streamtape.com/file/dlticket?file={file_id}&login={LOGIN}&key={KEY}").json()
    if res['status'] != 200: return print(f"❌ Ticket fail: {res.get('msg')}")
    
    time.sleep(res['result']['wait_time'])

    # 2. Get JSON Link
    dl_res = requests.get(f"https://api.streamtape.com/file/dl?file={file_id}&ticket={res['result']['ticket']}").json()
    if dl_res['status'] != 200: return print(f"❌ DL link fail")

    final_url = dl_res['result']['url']
    name = dl_res['result']['name']

    # 3. Aria2 Fast Download
    print(f"⬇️ Downloading: {name}")
    subprocess.run(["aria2c", "-x", "16", "-s", "16", "-o", name, final_url], check=True)

    # 4. Upload to HF
    print(f"⬆️ Uploading to HF {REPO_TYPE}...")
    api = HfApi(token=HF_TOKEN)
    api.upload_file(path_or_fileobj=name, path_in_repo=name, repo_id=REPO_ID, repo_type=REPO_TYPE)

    # 5. Sequential Cleanup (Save Disk Space)
    os.remove(name)
    print(f"✅ Finished: {name}")

if __name__ == "__main__":
    links = [l.strip() for l in LINKS_RAW.splitlines() if l.strip()]
    for link in links:
        try:
            process_file(link)
        except Exception as e:
            print(f"❌ Error on {link}: {e}")
