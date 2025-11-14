import os
import requests
import gdown
import subprocess
import re
import mediafire_dl
import time

def extract_google_drive_id(url):
    """
    Extracts the Google Drive file/folder ID from various URL formats.
    """
    drive_id_pattern = re.compile(r'drive.google.com/.*?(?:file/d/|drive/folders/|open\?id=|uc\?id=)([^/&?]+)')
    match = drive_id_pattern.search(url)
    if match:
        return match.group(1)
    else:
        return None

def download_file_from_katfile(url, output_path, apiKey="9368456hlxk1h9wdnydbob"):
    parts = url.split('/')
    domain = parts[2]
    filecode = parts[3]
    cloneurl = f"https://{domain}/api/file/clone?key={apiKey}&file_code={filecode}"
    response = requests.get(cloneurl)
    if response.status_code == 200:
        json_data = response.json()
        download_url = json_data.get('result', {}).get('url')
        parts_final = download_url.split('/')
        filecodex = parts_final[3]
        final_url = f"https://{domain}/api/file/direct_link?key={apiKey}&file_code={filecodex}"
        response = requests.get(final_url)
        if response.status_code == 200:
            json_data = response.json()
            download_url = json_data.get('result', {}).get('url')
            try:
                # Download the file using aria2c
                subprocess.run(['aria2c', '-x', '16', '-d', output_path, download_url], check=True)
                print(f"Downloaded: {download_url}")
            except Exception as e:
                print(f"Error downloading from Katfile: {str(e)}")
        else:
            print("Error while fetching Katfile API")
    else:
        print("Error while fetching Katfile API")


# --- Main Execution ---

# Get the raw list of links from the environment variable
links_content = os.getenv('LINKS_CONTENT')

if links_content:
    single_line_batch_links = links_content.splitlines()
    print(f"Loaded {len(single_line_batch_links)} links from environment variable.")
else:
    print("Error: LINKS_CONTENT environment variable not found or is empty.")
    single_line_batch_links = []


if single_line_batch_links:
    output_path = "source/"
    os.makedirs(output_path, exist_ok=True)
    current_dir = os.getcwd() # Get current directory to return to

    print(f"--- Starting Downloads to {output_path} ---")

    for url in single_line_batch_links:
        url = url.strip() # Clean up whitespace
        if not url: # Skip empty lines
            print("Skipping empty line.")
            continue
        
        print(f"\nProcessing URL: {url}")
        file_id = extract_google_drive_id(url)
        
        if file_id:
            # --- GDrive Logic (supports file/folder) ---
            try:
                print(f"Attempting GDrive download (subprocess): {file_id}")
                
                # 1. Change directory into the output folder
                os.chdir(output_path) 
                
                # 2. Run the command-line gdown
                subprocess.run(['gdown', file_id], check=True)
                
                # 3. Go back to the original directory
                os.chdir(current_dir) 
                print(f"Successfully downloaded GDrive file with ID: {file_id}")
                
            except Exception as e:
                # 4. Make SURE we go back to the original directory on error
                os.chdir(current_dir) 
                
                print(f"gdown subprocess failed ({str(e)}). Attempting as FOLDER...")
                try:
                    # Folder download still has to use the Python function
                    gdown.download_folder(id=file_id, output=output_path, quiet=False, resume=True)
                    print(f"Successfully downloaded GDrive folder with ID: {file_id}")
                except Exception as e2:
                    print(f"Error downloading {file_id} as both file and folder: {str(e2)}")
            # --- End of GDrive Logic ---

        elif "katfile.com" in url or "katfile.cloud" in url:
            # --- Katfile Logic (Checks for both domains) ---
            download_file_from_katfile(url, output_path)

        elif url.startswith("https://download") or "mediafire.com" in url:
            # --- Mediafire Logic ---
            try:
                print(f"Attempting Mediafire download: {url}")
                if url.startswith("https://download"):
                    url_parts = url.split("/")
                    new_url = f"https://www.mediafire.com/file/{url_parts[-2]}/{url_parts[-1]}"
                    mediafire_dl.download(new_url, output=output_path, quiet=False)
                else:
                    mediafire_dl.download(url, output=output_path, quiet=False)
                print(f"Successfully downloaded from Mediafire: {url}")
            except Exception as e:
                print(f"Error downloading from Mediafire: {str(e)}")
            # --- End of Mediafire Logic ---
            
        else:
            # --- Fallback to Aria2c ---
            try:
                filename = url.split('/')[-1].split('?')[0]
                if not filename:
                    filename = f"unknown_download_{int(time.time())}" # Added timestamp
                    
                print(f"Attempting download with aria2c as: {filename}")
                subprocess.run(['./aria2c', '-c', '-x', '16', '-d', output_path, '-o', filename, url], check=True)
                print(f"Downloaded: {filename}")
            except Exception as e:
                print(f"Error downloading {url} with aria2c: {str(e)}")
else:
    print("No links found in the links content.")

print("\n--- Download script finished. ---")
