import requests
import re

def extract_file_id(file_url):
    match = re.search(r'/file/([a-zA-Z0-9]{32})', file_url)
    if match:
        return match.group(1)
    return None

def rapidgator_login(email, password, code=None):
    url = "https://rapidgator.net/api/v2/user/login"
    params = {
        "login": email,
        "password": password
    }
    if code:
        params["code"] = code

    try:
        response = requests.get(url, params=params)
        data = response.json()

        if response.status_code == 200 and 'response' in data:
            token = data['response']['token']
            print(f"[✓] Login successful. Token: {token}")
            return token
        else:
            print("[✗] Login failed:", data.get("details", "No details"))
            return None
    except Exception as e:
        print(f"[!] Login error: {e}")
        return None

def get_download_url(token, file_id):
    url = "https://rapidgator.net/api/v2/file/download"
    params = {
        "token": token,
        "file_id": file_id
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()

        if response.status_code == 200 and data.get('response'):
            download_url = data['response']['download_url']
            print(f"[✓] Download URL: {download_url}")
            return download_url
        else:
            print("[✗] Failed to get download URL.")
            print("Details:", data.get("details", "No error details provided."))
            return None

    except Exception as e:
        print(f"[!] Error fetching download URL: {e}")
        return None

# === MAIN ===
if __name__ == "__main__":
    email = "kyawkaung709@gmail.com"
    password = "htz175039"
    file_url = "https://rapidgator.net/file/7f22691d8f17a81ca2f65d44c2c0cfb0/MyS15.part1.rar.html"
    code = None  # If you use 2FA, provide the code here

    file_id = extract_file_id(file_url)
    if not file_id:
        print("[✗] Invalid Rapidgator file URL")
    else:
        token = rapidgator_login(email, password, code)
        if token:
            get_download_url(token, file_id)
