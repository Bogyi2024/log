import os
import requests
import gdown
import subprocess
import re
import mediafire_dl


def fetch_links_from_pastebin(pastebin_link):
    response = requests.get(pastebin_link)
    if response.status_code == 200:
        return response.text.splitlines()
    else:
        print(f"Error fetching from Pastebin: {response.status_code}")
        return []

def extract_google_drive_id(url):
    drive_id_pattern = re.compile(r'(?:drive.google.com/.*?id=|drive.google.com/file/d/|drive.google.com/open\?id=|drive.google.com/uc\?id=)([a-zA-Z0-9_-]{33,})')
    match = drive_id_pattern.search(url)
    if match:
        return match.group(1)
    else:
        print(f"Invalid Google Drive URL: {url}")
        return None

def download_file_from_google_drive(file_id, output_path):
    try:
        gdrive_url = f"https://drive.google.com/uc?id={file_id}"
        gdown.download(gdrive_url, output=os.path.join(output_path, file_id), quiet=False)
        print(f"Downloaded: {gdrive_url}")
    except Exception as e:
        print(f"Error downloading from Google Drive: {str(e)}")

def download_file_from_mediafire(url, output_path):
    try:
        mediafire_dl.download(url, quiet=False, output=output_path)
        print(f"Downloaded: {url}")
    except Exception as e:
        print(f"Error downloading from Mediafire: {str(e)}")

def download_file_with_aria2c(url, output_path):
    filename = url.split('/')[-1]
    try:
        subprocess.run(['aria2c', '-x', '16', '-d', output_path, url], check=True)
        print(f"Downloaded: {filename}")
    except Exception as e:
        print(f"Error downloading {filename}: {str(e)}")

#def download_file_from_katfile(url, output_path, apiKey="699996yph6h88a7rc6c1g8"):
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

def main():
    pastebin_link = "https://pastebin.com/raw/DZFuWkZP"
    single_line_batch_links = fetch_links_from_pastebin(pastebin_link)

    if single_line_batch_links:
        output_path = "download/"
        os.makedirs(output_path, exist_ok=True)

        for url in single_line_batch_links:
            url = url.strip()  # Strip whitespace
            if not url:
                print("Empty URL encountered")
                continue

            file_id = extract_google_drive_id(url)
            if file_id:
                download_file_from_google_drive(file_id, output_path)
            elif url.startswith("https://download") or "mediafire.com" in url:
                if url.startswith("https://download"):
                    url_parts = url.split("/")
                    new_url = f"https://www.mediafire.com/file/{url_parts[-2]}/{url_parts[-1]}"
                    download_file_from_mediafire(new_url, output_path)
                else:
                    download_file_from_mediafire(url, output_path)
            elif "katfile.com" in url:
                download_file_from_katfile(url, output_path)
            else:
                download_file_with_aria2c(url, output_path)
    else:
        print("No links found in the Pastebin link.")

if __name__ == "__main__":
    main()
