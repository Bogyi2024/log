import os
import requests
import subprocess

single_line_batch_links = "https://katfile.com/0to3nid6r6k9/415167_3xplanet_Uncen-leaked_WANZ-894.part1.rar.html"  # @param {type:"string"}

perlink = single_line_batch_links.split(" ")

if single_line_batch_links != "":
    files = perlink

os.mkdir("download")

for url in files:
    if url == "":
        continue
    else:
        output_path = "download/"  # @param {type:"string"}
        apiKey = "699996yph6h88a7rc6c1g8"
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
                
                if download_url:
                    # Construct the command for curl
                    local_filename = os.path.join(output_path, download_url.split('/')[-1])
                    command = ['curl', '-o', local_filename, download_url]
                    subprocess.run(command, check=True)
                    print(f"Downloaded: {local_filename}")
            else:
                print("Error while fetching direct link from Katfile API")
        else:
            print("Error while fetching clone link from Katfile API")
