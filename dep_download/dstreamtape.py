import requests
import time
import os
import sys
from tqdm import tqdm
from huggingface_hub import HfApi

# --- CONFIGURATION ---
LOGIN = os.environ.get("ST_LOGIN")
API_KEY = os.environ.get("ST_KEY")
HF_TOKEN = os.environ.get("HF_TOKEN")
HF_REPO_ID = os.environ.get("HF_REPO_ID")
HF_REPO_TYPE = os.environ.get("HF_REPO_TYPE", "model")
LINKS_RAW = os.environ.get("ST_LINKS", "")
LINKS = [l.strip() for l in LINKS_RAW.splitlines() if l.strip()]

if not LOGIN or not API_KEY:
    print("❌ Error: ST_LOGIN and ST_KEY are required.")
    sys.exit(1)

def extract_file_id(url):
    if "/v/" in url:
        return url.split("/v/")[1].split("/")[0]
    elif "/e/" in url:
        return url.split("/e/")[1].split("/")[0]
    return url

def process_file(file_id):
    print(f"\n🚀 Processing: {file_id}")
    
    # 1. GET THE TICKET
    ticket_url = f"https://api.streamtape.com/file/dlticket?file={file_id}&login={LOGIN}&key={API_KEY}"
    ticket_resp = requests.get(ticket_url).json()

    if ticket_resp.get('status') != 200:
        print(f"❌ Ticket Error: {ticket_resp.get('msg')}")
        return

    ticket = ticket_resp['result']['ticket']
    wait_time = ticket_resp['result']['wait_time']
    
    print(f"⏳ Waiting {wait_time} seconds (API Requirement)...")
    time.sleep(wait_time)

    # 2. REQUEST THE DOWNLOAD URL
    dl_url = f"https://api.streamtape.com/file/dl?file={file_id}&ticket={ticket}"
    dl_resp = requests.get(dl_url).json()

    if dl_resp.get('status') != 200:
        print(f"❌ DL URL Error: {dl_resp.get('msg')}")
        return

    # Extract final storage URL and filename from JSON result
    final_url = dl_resp['result']['url']
    filename = dl_resp['result']['name']
    
    print(f"🔗 Final Storage Link Found.")
    
    # 3. DOWNLOAD
    print(f"⬇️ Downloading: {filename}")
    try:
        with requests.get(final_url, stream=True) as r:
            r.raise_for_status()
            total_size = int(r.headers.get('content-length', 0))
            
            with open(filename, 'wb') as f, tqdm(
                desc=filename,
                total=total_size,
                unit='B',
                unit_scale=True,
                unit_divisor=1024,
            ) as bar:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
                    bar.update(len(chunk))
    except Exception as e:
        print(f"❌ Download Failed: {e}")
        if os.path.exists(filename): os.remove(filename)
        return

    # 4. UPLOAD TO HF
    print(f"⬆️ Uploading to HF {HF_REPO_TYPE}: {HF_REPO_ID}")
    api = HfApi(token=HF_TOKEN)
    try:
        api.upload_file(
            path_or_fileobj=filename,
            path_in_repo=filename,
            repo_id=HF_REPO_ID,
            repo_type=HF_REPO_TYPE
        )
        print(f"✅ Upload Finished!")
    except Exception as e:
        print(f"❌ Upload Failed: {e}")

    # 5. CLEANUP (Delete file to free runner space)
    if os.path.exists(filename):
        os.remove(filename)
        print("🧹 Local file deleted.")

# --- MAIN LOOP ---
print(f"📋 Found {len(LINKS)} links.")
for link in LINKS:
    fid = extract_file_id(link)
    try:
        process_file(fid)
    except Exception as e:
        print(f"❌ Critical error on link {link}: {e}")
