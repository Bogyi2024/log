import os
import requests
import gdown
import subprocess
import re
import mediafire_dl
from time import sleep

# --- CONFIGURATION (UPDATED TO USE HARDCODED VALUES) ---
# Hardcoded Rapidgator Login Credentials
LOGIN_EMAIL = "sdserver200@gmail.com"
PASSWORD = "kk123456"
TWO_FACTOR_CODE = ''
# Default Pastebin link (still prefers environment variable if set, otherwise uses default)
PASTEBIN_LINK = os.environ.get('PASTEBIN_URL', "https://pastebin.com/raw/EBiRrTGp?nocache=1")
# Hardcoded Output Path
OUTPUT_PATH = "download"
# Hardcoded Katfile API Key
KATFILE_API_KEY = "9368456hlxk1h9wdnydbob"

# --- UTILITY FUNCTIONS ---

def resolve_short_url(url):
    """Resolves shortened links like tinyurl, bit.ly using a HEAD request."""
    try:
        # Use a timeout and allow redirects
        response = requests.head(url, allow_redirects=True, timeout=10)
        response.raise_for_status()
        final_url = response.url
        if final_url != url:
            print(f"Resolved {url} -> {final_url}")
        return final_url
    except requests.exceptions.RequestException as e:
        print(f"Failed to resolve short URL {url}: {e}")
        return url

def fetch_links_from_pastebin(pastebin_link):
    """Fetches raw lines from a Pastebin link."""
    try:
        print(f"Fetching links from: {pastebin_link}")
        response = requests.get(pastebin_link, timeout=15)
        response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)
        # Return a list of non-empty, stripped lines
        return [line.strip() for line in response.text.splitlines() if line.strip()]
    except Exception as e:
        print(f"Error fetching links from Pastebin: {e}")
        return []

def extract_google_drive_id(url):
    """Extracts the file ID from various Google Drive URL formats."""
    # Pattern includes common formats and looks for the long ID string
    drive_id_pattern = re.compile(r'(?:drive.google.com/.*?id=|drive.google.com/file/d/|drive.google.com/open\?id=|drive.google.com/uc\?id=)([a-zA-Z0-9_-]{33,})')
    match = drive_id_pattern.search(url)
    if match:
        return match.group(1)
    return None

# --- DOWNLOAD FUNCTIONS ---

def download_file_from_google_drive(file_id, output_path):
    """Downloads a file using the gdown library."""
    gdrive_url = f"https://drive.google.com/uc?id={file_id}"
    print(f"Attempting Google Drive download: {gdrive_url}")
    try:
        # gdown will handle the file name correctly if the folder is specified
        gdown.download(gdrive_url, output=output_path, quiet=False)
        print(f"Successfully downloaded file ID: {file_id}")
    except Exception as e:
        print(f"Error downloading from Google Drive ({file_id}): {str(e)}")

def download_file_from_mediafire(url, output_path):
    """Downloads a file using the mediafire_dl library."""
    print(f"Attempting Mediafire download: {url}")
    try:
        # mediafire_dl handles the actual download path and filename
        mediafire_dl.download(url, quiet=False, output=output_path)
        print(f"Successfully downloaded from Mediafire: {url}")
    except Exception as e:
        print(f"Error downloading from Mediafire ({url}): {str(e)}")

def rapidgator_login(email, password, code=''):
    """Logs into Rapidgator and returns the session token."""
    print("Attempting Rapidgator login...")
    login_url = 'https://rapidgator.net/api/v2/user/login'
    login_params = {
        'login': email,
        'password': password,
        'code': code
    }
    try:
        response = requests.get(login_url, params=login_params, timeout=10)
        data = response.json()
        if response.status_code == 200 and data.get('response'):
            token = data['response']['token']
            print('Rapidgator login successful.')
            return token
        else:
            print('Rapidgator login failed:', data.get('details', 'Unknown error'))
            return None
    except Exception as e:
        print(f"Rapidgator login error: {e}")
        return None

def extract_rapidgator_file_id(resolved_url):
    """Extracts the 32-character Rapidgator file ID from a resolved URL."""
    match = re.search(r'/file/([a-zA-Z0-9]{32})', resolved_url)
    if match:
        return match.group(1)
    return None

def download_file_from_rapidgator(file_id, token, output_path):
    """Gets download link from Rapidgator API and uses aria2c to download."""
    info_url = 'https://rapidgator.net/api/v2/file/info'
    download_url_api = 'https://rapidgator.net/api/v2/file/download'

    # 1. Get file info
    info_params = {'file_id': file_id, 'token': token}
    try:
        info_response = requests.get(info_url, params=info_params, timeout=10)
        info_data = info_response.json()
        if not (info_response.status_code == 200 and info_data.get('response')):
            print(f"Failed to get info for {file_id}. Details: {info_data.get('details', 'N/A')}")
            return
        
        filename = info_data['response']['file']['name']
        print(f"File found: {filename}")
    except Exception as e:
        print(f"Failed to get info for {file_id}: {e}")
        return

    # 2. Get download URL
    download_params = {'file_id': file_id, 'token': token}
    try:
        dl_response = requests.get(download_url_api, params=download_params, timeout=10)
        dl_data = dl_response.json()
        if dl_response.status_code == 200 and dl_data.get('response'):
            download_link = dl_data['response']['download_url']
            print(f"Retrieved download link for {filename}. Starting download...")
        else:
            print(f"Failed to get download URL for {filename}. Details: {dl_data.get('details', 'N/A')}")
            return
    except Exception as e:
        print(f"Failed to get download URL: {e}")
        return

    # 3. Download using aria2c
    try:
        subprocess.run([
            'aria2c', '-x', '16', # Use 16 connections for faster download
            '-d', output_path,
            '-o', filename,
            download_link
        ], check=True)
        print(f"Successfully downloaded: {filename}")
    except subprocess.CalledProcessError as e:
        print(f"aria2c failed for {filename}: {e}")

def download_file_from_katfile(url, output_path, apiKey=KATFILE_API_KEY):
    """Downloads a file from Katfile using the API key to get a direct link."""
    print(f"Attempting Katfile download: {url}")
    try:
        parts = url.split('/')
        domain = parts[2]
        filecode = parts[3]

        # Step 1: Clone the file (necessary for some hosts)
        cloneurl = f"https://{domain}/api/file/clone?key={apiKey}&file_code={filecode}"
        response = requests.get(cloneurl, timeout=10)
        response.raise_for_status()
        json_data = response.json()
        download_url_base = json_data.get('result', {}).get('url')

        if not download_url_base:
            print(f"Katfile API (Clone) error: {json_data.get('msg', 'URL not found in response')}")
            return

        # Extract the new filecode from the cloned URL (as in original script logic)
        parts_final = download_url_base.split('/')
        filecodex = parts_final[3]
        
        # Step 2: Get the direct download link
        final_api_url = f"https://{domain}/api/file/direct_link?key={apiKey}&file_code={filecodex}"
        response = requests.get(final_api_url, timeout=10)
        response.raise_for_status()
        json_data = response.json()
        download_url_direct = json_data.get('result', {}).get('url')

        if not download_url_direct:
            print(f"Katfile API (Direct Link) error: {json_data.get('msg', 'Direct URL not found')}")
            return
        
        # Step 3: Download using aria2c
        subprocess.run(['aria2c', '-x', '16', '-d', output_path, download_url_direct], check=True)
        print(f"Successfully downloaded from Katfile: {download_url_direct}")

    except Exception as e:
        print(f"Error downloading from Katfile ({url}): {str(e)}")

def download_file_with_aria2c(url, output_path):
    """Uses aria2c for generic downloads (HTTP/FTP)."""
    filename = url.split('/')[-1]
    print(f"Attempting generic download with aria2c: {filename}")
    try:
        subprocess.run(['aria2c', '-x', '16', '-d', output_path, url], check=True)
        print(f"Successfully downloaded: {filename}")
    except Exception as e:
        print(f"Error downloading {filename} using aria2c: {str(e)}")

# --- MAIN EXECUTION ---

def main():
    # 1. Setup
    os.makedirs(OUTPUT_PATH, exist_ok=True)

    # 2. Rapidgator Login (only if credentials provided)
    rg_token = None
    if LOGIN_EMAIL and PASSWORD:
        rg_token = rapidgator_login(LOGIN_EMAIL, PASSWORD, TWO_FACTOR_CODE)

    # 3. Fetch all links
    raw_links = fetch_links_from_pastebin(PASTEBIN_LINK)

    if not raw_links:
        print("No valid links found. Exiting.")
        return

    # 4. Process and Download Links
    for i, url in enumerate(raw_links):
        print(f"\n--- Processing Link {i+1}/{len(raw_links)}: {url} ---")
        
        # A. Resolve short URLs first
        resolved_url = resolve_short_url(url)
        
        if not resolved_url:
            print(f"Skipping link {url} due to resolution failure.")
            continue

        # B. Check for known hosts
        
        # B1. Rapidgator Check (Requires token)
        if "rapidgator.net" in resolved_url:
            rg_file_id = extract_rapidgator_file_id(resolved_url)
            if rg_file_id and rg_token:
                download_file_from_rapidgator(rg_file_id, rg_token, OUTPUT_PATH)
            else:
                print("Skipping Rapidgator link: Login failed or file ID not found.")
            continue

        # B2. Google Drive Check
        file_id = extract_google_drive_id(resolved_url)
        if file_id:
            download_file_from_google_drive(file_id, OUTPUT_PATH)
            continue

        # B3. Mediafire Check
        if resolved_url.startswith("https://download") or "mediafire.com" in resolved_url:
            # Handle the 'https://download.../' to 'https://www.mediafire.com/file/...' conversion
            if resolved_url.startswith("https://download"):
                url_parts = resolved_url.split("/")
                mf_url = f"https://www.mediafire.com/file/{url_parts[-2]}/{url_parts[-1]}"
            else:
                mf_url = resolved_url
            download_file_from_mediafire(mf_url, OUTPUT_PATH)
            continue
            
        # B4. Katfile Check
        if "katfile.com" in resolved_url:
            download_file_from_katfile(resolved_url, OUTPUT_PATH)
            continue

        # C. Generic Download (Last Resort)
        print("Host not recognized. Defaulting to generic aria2c download.")
        download_file_with_aria2c(resolved_url, OUTPUT_PATH)
        
        # Adding a small delay to avoid hammering hosts or APIs
        sleep(2) 

    print("\n--- All links processed. ---")

if __name__ == "__main__":
    main()
