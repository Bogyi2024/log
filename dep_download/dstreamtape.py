import requests
import time
import os
import sys
from tqdm import tqdm
from huggingface_hub import HfApi

# --- CONFIGURATION (Synced with the latest GitHub Workflow) ---
# We use .get() to avoid crashes if a variable is missing
LOGIN = os.environ.get("ST_LOGIN")
API_KEY = os.environ.get("ST_KEY")
HF_TOKEN = os.environ.get("HF_TOKEN")
HF_REPO_ID = os.environ.get("HF_REPO_ID")
HF_REPO_TYPE = os.environ.get("HF_REPO_TYPE", "space")  # New: reads from UI dropdown
LINKS_RAW = os.environ.get("ST_LINKS", "")             # New: matches workflow 'ST_LINKS'
LINKS = [l.strip() for l in LINKS_RAW.splitlines() if l.strip()]

if not LOGIN or not API_KEY:
    print("❌ Error: ST_LOGIN and ST_KEY are required.")
    sys.exit(1)

def download_and_upload(file_id):
    print(f"\n🚀 Processing File ID: {file_id}")
    
    # 1. GET THE TICKET
    ticket_url = f"https://api.streamtape.com/file/dlticket?file={file_id}&login={LOGIN}&key={API_KEY}"
    try:
        ticket_resp = requests.get(ticket_url).json()
    except Exception as e:
        print(f"❌ Connection Error (Ticket): {e}")
        return

    if ticket_resp.get('status') != 200:
        print(f"❌ Ticket Error: {ticket_resp.get('msg')}")
        return

    dticket = ticket_resp['result']['ticket']
    wait_time = ticket_resp['result']['wait_time']
    
    print(f"⏳ Waiting {wait_time} seconds...")
    time.sleep(wait_time)

    # 2. REQUEST THE DOWNLOAD URL
    dl_request_url = f"https://api.streamtape.com/file/dl?file={file_id}&ticket={dticket}"
    try:
        dl_resp = requests.get(dl_request_url).json()
    except Exception as e:
        print(f"❌ Connection Error (DL URL): {e}")
        return

    if dl_resp.get('status') != 200:
        print(f"❌ DL URL Error: {dl_resp.get('msg')}")
        return

    final_file_url = dl_resp['result']['url']
    filename = dl_resp['result']['name']
    
    print(f"🔗 Final Storage Link: {final_file_url}")
    print(f"⬇️ Downloading: {filename}")

    # 3. START ACTUAL DOWNLOAD
    try:
        with requests.get(final_file_url, stream=True) as r:
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
        print(f"✅ Download Finished: {filename}")
    except Exception as e:
        print(f"❌ Download Failed: {e}")
        if os.path.exists(filename): os.remove(filename)
        return

    # 4. UPLOAD TO HUGGING FACE
    if HF_TOKEN and HF_REPO_ID:
        # Use the Repo Type (space, dataset, or model) from the UI
        print(f"⬆️ Uploading to Hugging Face {HF_REPO_TYPE}: {HF_REPO_ID}")
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
    else:
        print("⚠️ Skipping Upload: HF_TOKEN or HF_REPO_ID missing.")

    # Cleanup
    if os.path.exists(filename):
        os.remove(filename)
        print("🧹 Cleaned up local file.")

def extract_file_id(url):
    if "/v/" in url:
        return url.split("/v/")[1].split("/")[0]
    elif "/e/" in url:
        return url.split("/e/")[1].split("/")[0]
    return url

# --- MAIN LOOP ---
print(f"📋 Found {len(LINKS)} links to process.")
for link in LINKS:
    file_id = extract_file_id(link)
    download_and_upload(file_id)
