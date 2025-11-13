import os
import gdown
import subprocess
import re
import mediafire_dl
import time  # <-- ADDED THIS IMPORT

def extract_google_drive_id(url):
    """
    Extracts the Google Drive file/folder ID from various URL formats.
    """
    # This pattern matches /file/d/ID, /uc?id=ID, /open?id=ID, and /drive/folders/ID
    drive_id_pattern = re.compile(r'drive.google.com/.*?(?:file/d/|drive/folders/|open\?id=|uc\?id=)([^/&?]+)')
    match = drive_id_pattern.search(url)
    if match:
        return match.group(1)
    else:
        return None

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

    for url in single_line_batch_links:
        url = url.strip() # Clean up whitespace
        if not url: # Skip empty lines
            continue
            
        file_id = extract_google_drive_id(url)
        
        if file_id:
            # --- THIS IS THE NEW RETRY LOGIC ---
            download_success = False
            for attempt in range(3): # Try 3 times
                try:
                    # 1. Try as a FILE first
                    gdrive_url = f"https://drive.google.com/uc?id={file_id}"
                    print(f"Attempt {attempt + 1}/3 as FILE: {gdrive_url}")
                    
                    gdown.download(url=gdrive_url, output=output_path, quiet=False, fuzzy=True, resume=True)
                    
                    print(f"Successfully downloaded file with ID: {file_id}")
                    download_success = True
                    break # Exit the retry loop if successful
                    
                except Exception as e:
                    print(f"File attempt {attempt + 1} failed ({str(e)}).")
                    
                    # Check for the '.part already exists' error
                    if "already exists" in str(e):
                         print("Cleaning up partial file and retrying...")
                         # Try to parse the .part file path from the error and remove it
                         try:
                             part_file = re.search(r"Destination path '(.*?)'", str(e)).group(1)
                             if os.path.exists(part_file):
                                 os.remove(part_file)
                                 print(f"Removed: {part_file}")
                         except Exception as re_e:
                             # This inner try/except catches errors in parsing the error string itself
                             print(f"Could not parse/remove partial file: {re_e}")
                    
                    if attempt < 2: # Don't sleep on the last attempt
                        print("Waiting 5 seconds before retrying...")
                        time.sleep(5) # Wait 5 seconds

            # If all file attempts failed, try as a FOLDER
            if not download_success:
                print("All file attempts failed. Attempting as FOLDER...")
                try:
                    gdown.download_folder(id=file_id, output=output_path, quiet=False, resume=True)
                    print(f"Successfully downloaded folder with ID: {file_id}")
                except Exception as e2:
                    print(f"Error downloading {file_id} as both file and folder: {str(e2)}")
            # --- END OF RETRY LOGIC ---
            
        else:
            # If it's not a GDrive link, try Mediafire or Aria2c
            if url.startswith("https://download") or "mediafire.com" in url:
                try:
                    os.chdir(output_path) # Go into the source folder
                    if url.startswith("https://download"):
                        url_parts = url.split("/")
                        new_url = f"https://www.mediafire.com/file/{url_parts[-2]}/{url_parts[-1]}"
                        mediafire_dl.download(new_url, quiet=False)
                    else:
                        mediafire_dl.download(url, quiet=False)
                    os.chdir(current_dir) # Go back to the original directory
                    print(f"Downloaded: {url}")
                except Exception as e:
                    print(f"Error downloading from Mediafire: {str(e)}")
                    os.chdir(current_dir) # Ensure we go back up even on error
            else:
                # Fallback to aria2c for other direct links
                filename = url.split('/')[-1].split('?')[0] # Get filename before query params
                if not filename:
                    filename = "unknown_download"
                    
                filepath = os.path.join(output_path, filename)
                try:
                    # Added -c to allow resume
                    subprocess.run(['./aria2c', '-c', '-x', '16', '-d', output_path, '-o', filename, url], check=True)
                    print(f"Downloaded: {filename}")
                except Exception as e:
                    print(f"Error downloading {filename}: {str(e)}")
else:
    print("No links found in the links content.")

print("Download script finished.")
