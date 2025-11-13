import os
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
            # --- NEW LOGIC: CALL GDOWN VIA SUBPROCESS ---
            try:
                print(f"Attempting download via gdown (subprocess): {file_id}")
                
                # 1. Change directory into the output folder
                os.chdir(output_path) 
                
                # 2. Run the command-line gdown (which you proved works)
                # We add --fuzzy and --resume for reliability
                subprocess.run(
                    ['gdown', file_id], 
                    check=True
                )
                
                # 3. Go back to the original directory
                os.chdir(current_dir) 
                print(f"Successfully downloaded file with ID: {file_id}")
                
            except Exception as e:
                # 4. Make SURE we go back to the original directory on error
                os.chdir(current_dir) 
                
                print(f"gdown subprocess failed ({str(e)}). Attempting as FOLDER...")
                try:
                    # Folder download still has to use the Python function
                    gdown.download_folder(id=file_id, output=output_path, quiet=False, resume=True)
                    print(f"Successfully downloaded folder with ID: {file_id}")
                except Exception as e2:
                    print(f"Error downloading {file_id} as both file and folder: {str(e2)}")
            # --- END OF NEW LOGIC ---
            
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
                try:
                    # We can use the -o flag to set the filename for non-gdrive links
                    filename = url.split('/')[-1].split('?')[0]
                    if not filename:
                        filename = "unknown_download"
                        
                    subprocess.run(['./aria2c', '-c', '-x', '16', '-d', output_path, '-o', filename, url], check=True)
                    print(f"Downloaded: {filename}")
                except Exception as e:
                    print(f"Error downloading {url}: {str(e)}")
else:
    print("No links found in the links content.")

print("Download script finished.")
