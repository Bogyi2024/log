import os
import gdown
import subprocess
import re
import mediafire_dl
import time
import sys

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
            
        print(f"\n--- Processing URL: {url} ---")
            
        file_id = extract_google_drive_id(url)
            
        if file_id:
            # --- GOOGLE DRIVE LOGIC (Uses gdown Python API with file ID) ---
            try:
                print(f"Attempting download via gdown (file ID): {file_id}")
                
                gdown.download(id=file_id, output=output_path, quiet=False)
                
                print(f"Successfully downloaded file with ID: {file_id}")
                
            except Exception as e:
                print(f"gdown file download failed ({str(e)}). Attempting as FOLDER...")
                try:
                    # Folder download falls back to the Python gdown function
                    gdown.download_folder(id=file_id, output=output_path, quiet=False, resume=True)
                    print(f"Successfully downloaded folder with ID: {file_id}")
                except Exception as e2:
                    print(f"Error downloading {file_id} as both file and folder: {str(e2)}")

        elif "msubb2.net" in url:
            # --- WGET LOGIC (Handles msubb2.net links) ---
            print(f"Attempting download via wget (msubb2.net): {url}")
            try:
                subprocess.run(
                    ['wget', '-P', output_path, url],
                    check=True
                )
                print(f"Successfully downloaded msubb2.net link via wget.")
            except subprocess.CalledProcessError as e:
                print(f"wget download failed (Exit Code {e.returncode}). Error: {e}")
            except FileNotFoundError:
                print("Error: 'wget' command not found. Ensure wget is installed and in your system PATH.")
            except Exception as e:
                print(f"An unexpected error occurred during wget download: {str(e)}")

        elif "workers" in url:
            # --- CURL LOGIC (NEW: Handles auto-naming with Content-Disposition) ---
            print(f"Attempting download via curl (auto-name/Content-Disposition): {url}")
            try:
                os.chdir(output_path)
                
                # We use -O to save the file and -J to use the server's Content-Disposition filename
                subprocess.run(
                    ['curl', '-O', '-J', url],
                    check=True
                )
                
                print(f"Successfully downloaded 'workers' link via curl.")
                
            except subprocess.CalledProcessError as e:
                print(f"Curl download failed (Exit Code {e.returncode}). Error: {e}")
            except FileNotFoundError:
                print("Error: 'curl' command not found. Ensure curl is installed and in your system PATH.")
            except Exception as e:
                print(f"An unexpected error occurred during curl download: {str(e)}")
            finally:
                # Always go back to the original directory
                if os.getcwd() != current_dir:
                    os.chdir(current_dir)


        elif url.startswith("https://download") or "mediafire.com" in url:
            # --- MEDIAFIRE LOGIC (Uses mediafire_dl library) ---
            try:
                os.chdir(output_path) # Go into the source folder
                
                if url.startswith("https://download"):
                    # Convert raw Mediafire download link back to viewable file link
                    url_parts = url.split("/")
                    # Assumes format like: https://downloadXXX/YYYY/filekey/filename
                    if len(url_parts) >= 6:
                        new_url = f"https://www.mediafire.com/file/{url_parts[-2]}/{url_parts[-1]}"
                        mediafire_dl.download(new_url, quiet=False)
                    else:
                        print("Mediafire raw link format not recognized, skipping.")
                else:
                    mediafire_dl.download(url, quiet=False)
                    
                print(f"Downloaded: {url}")
            except Exception as e:
                print(f"Error downloading from Mediafire: {str(e)}")
            finally:
                # Always go back to the original directory
                if os.getcwd() != current_dir:
                    os.chdir(current_dir)
                    
        else:
            # --- FALLBACK LOGIC (Uses aria2c for generic direct links) ---
            try:
                # Fallback uses aria2c. We must manually guess the filename here.
                filename = url.split('/')[-1].split('?')[0]
                if not filename or '.' not in filename: # Simple check for a proper filename
                    filename = "unknown_download"
                        
                print(f"Attempting download via aria2c for generic link (Manually named: {filename})")
                    
                # Note: We must specify the full path for the output file when not changing directory
                full_output_file = os.path.join(output_path, filename)
                
                subprocess.run(
                    ['./aria2c', '-c', '-x', '16', '-o', full_output_file, url], 
                    check=True
                )
                print(f"Downloaded: {full_output_file}")
            except Exception as e:
                print(f"Error downloading {url} via aria2c: {str(e)}")

else:
    print("No links found in the links content.")

print("\nDownload script finished.")
