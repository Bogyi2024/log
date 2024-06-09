import requests
import subprocess
import re

# Function to fetch links from Pastebin and extract file IDs
def fetch_links_from_pastebin(pastebin_link):
    response = requests.get(pastebin_link)
    if response.status_code == 200:
        urls = response.text.strip().split('\n')
        file_ids = [re.search(r'/file/([a-z0-9]+)/', url).group(1) for url in urls if re.search(r'/file/([a-z0-9]+)/', url)]
        return file_ids
    else:
        print("Error fetching links from Pastebin")
        return []

# User credentials
login_email = 'sdserver200@gmail.com'
password = 'kk123456'
two_factor_code = ''  # Leave empty if 2FA is not enabled

# URLs
login_url = 'https://rapidgator.net/api/v2/user/login'
info_url = 'https://rapidgator.net/api/v2/file/info'
download_url = 'https://rapidgator.net/api/v2/file/download'

# Step 1: Log in to get the access token
login_params = {
    'login': login_email,
    'password': password,
    'code': two_factor_code
}

login_response = requests.get(login_url, params=login_params)
login_data = login_response.json()

if login_response.status_code == 200 and login_data.get('response'):
    token = login_data['response']['token']
    print('Login successful. Token:', token)

    # Fetch file IDs from Pastebin
    pastebin_link = "https://pastebin.com/raw/EBiRrTGp"
    file_ids = fetch_links_from_pastebin(pastebin_link)

    for file_id in file_ids:
        # Step 2: Get the file info
        info_params = {
            'file_id': file_id,
            'token': token
        }

        info_response = requests.get(info_url, params=info_params)
        info_data = info_response.json()

        if info_response.status_code == 200 and info_data.get('response'):
            file_info = info_data['response']['file']
            print('File Info:', file_info)

            # Step 3: Get the download URL
            download_params = {
                'file_id': file_id,
                'token': token
            }
            
            download_response = requests.get(download_url, params=download_params)
            download_data = download_response.json()

            if download_response.status_code == 200 and download_data.get('response'):
                download_link = download_data['response']['download_url']
                print('Download URL:', download_link)

                # Step 4: Download the file using aria2c
                filename = file_info['name']
                output_path = '.'  # Change to your desired output directory

                try:
                    subprocess.run(['aria2c', '-x', '16', '-d', output_path, '-o', filename, download_link], check=True)
                    print(f'Download successful: {filename}')
                except subprocess.CalledProcessError as e:
                    print(f'Error during download: {e}')
            else:
                print('Failed to get download URL:', download_response.status_code, download_data)
        else:
            print('Failed to get file info:', info_response.status_code, info_data)
else:
    print('Login failed:', login_response.status_code, login_data)
