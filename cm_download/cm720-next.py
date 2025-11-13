import os
import gdown
import subprocess
import re
import mediafire_dl

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

    for url in single_line_batch_links:
        url = url.strip() # Clean up whitespace
        if not url: # Skip empty lines
            continue
            
        file_id = extract_google_drive_id(url)
        if file_id:
            try:
                # --- THIS IS THE CORRECTED SECTION ---
                # Pass the directory 'output_path' to 'output'.
                # gdown will automatically find the real filename.
                #gdown.download(id=file_id, output=output_path, quiet=False)
                gdown.download(id=file_id, output=output_path, quiet=False, fuzzy=True, resume=True)
                # --- END OF CORRECTION ---
                
                print(f"Downloaded Google Drive file with ID: {file_id}")
            except Exception as e:
                print(f"Error downloading from Google Drive (ID: {file_id}): {str(e)}")
        else:
            # If it's not a GDrive link, try Mediafire or Aria2c
            if url.startswith("https://download") or "mediafire.com" in url:
                try:
                    os.chdir(output_path)
                    if url.startswith("https://download"):
                        url_parts = url.split("/")
                        new_url = f"https://www.mediafire.com/file/{url_parts[-2]}/{url_parts[-1]}"
                        mediafire_dl.download(new_url, quiet=False)
                    else:
                        mediafire_dl.download(url, quiet=False)
                    os.chdir("../") # Go back up from 'source'
                    print(f"Downloaded: {url}")
                except Exception as e:
                    print(f"Error downloading from Mediafire: {str(e)}")
                    os.chdir("../") # Ensure we go back up even on error
            else:
                # Fallback to aria2c for other direct links
                filename = url.split('/')[-1].split('?')[0] # Get filename before query params
                if not filename:
                    filename = "unknown_download"
                    
                filepath = os.path.join(output_path, filename)
                try:
                    subprocess.run(['./aria2c', '-x', '16', '-d', output_path, '-o', filename, url], check=True)
                    print(f"Downloaded: {filename}")
                except Exception as e:
                    print(f"Error downloading {filename}: {str(e)}")
else:
    print("No links found in the links content.")

