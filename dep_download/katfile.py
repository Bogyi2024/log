import os
import requests
import subprocess

# Constants
PASTEBIN_LINK = "https://pastebin.com/raw/DZFuWkZP"
API_KEY = "699996yph6h88a7rc6c1g8"
OUTPUT_PATH = "download/"

def fetch_links_from_pastebin(pastebin_link):
    response = requests.get(pastebin_link)
    if response.status_code == 200:
        return response.text.strip().split('\n')
    else:
        print(f"Error fetching links from Pastebin: {response.status_code}")
        return []

def fetch_clone_url(domain, filecode, api_key):
    clone_url = f"https://{domain}/api/file/clone?key={api_key}&file_code={filecode}"
    response = requests.get(clone_url)
    if response.status_code == 200:
        json_data = response.json()
        return json_data.get('result', {}).get('url')
    else:
        print(f"Error fetching clone link: {response.status_code}")
        return None

def fetch_direct_link(domain, filecodex, api_key):
    final_url = f"https://{domain}/api/file/direct_link?key={api_key}&file_code={filecodex}"
    response = requests.get(final_url)
    if response.status_code == 200:
        json_data = response.json()
        return json_data.get('result', {}).get('url')
    else:
        print(f"Error fetching direct link: {response.status_code}")
        return None

def download_file(download_url, output_path):
    if download_url:
        local_filename = os.path.join(output_path, download_url.split('/')[-1])
        command = ['curl', '-o', local_filename, download_url]
        try:
            subprocess.run(command, check=True)
            print(f"Downloaded: {local_filename}")
        except subprocess.CalledProcessError as e:
            print(f"Error downloading {local_filename}: {e}")
    else:
        print("No download URL provided")

def process_katfile_links(katfile_links):
    os.makedirs(OUTPUT_PATH, exist_ok=True)

    for url in katfile_links:
        if url:
            parts = url.split('/')
            if len(parts) < 4:
                print(f"Invalid URL format: {url}")
                continue

            domain = parts[2]
            filecode = parts[3]

            clone_url = fetch_clone_url(domain, filecode, API_KEY)
            if clone_url:
                parts_final = clone_url.split('/')
                if len(parts_final) < 4:
                    print(f"Invalid clone URL format: {clone_url}")
                    continue

                filecodex = parts_final[3]
                download_url = fetch_direct_link(domain, filecodex, API_KEY)
                download_file(download_url, OUTPUT_PATH)

def main():
    katfile_links = fetch_links_from_pastebin(PASTEBIN_LINK)
    if katfile_links:
        process_katfile_links(katfile_links)
    else:
        print("No links found in the Pastebin link.")

if __name__ == "__main__":
    main()
