import os
import re
import requests
import subprocess

single_line_batch_links = "https://katfile.com/wa7vuxtwbe9u/415169_3xplanet_Uncen-leaked_YSN-365.part1.rar.html" # @param {type:"string"}

# Splitting the link by space might not be necessary since it contains only one link
# perlink = single_line_batch_links.split(" ")

# if single_line_batch_links != "":
#     files = perlink
# else:
#     file_url1 = "" # @param {type:"string"}
#     file_url2 = "" # @param {type:"string"}
#     file_url3 = "" # @param {type:"string"}
#     file_url4 = "" # @param {type:"string"}
#     file_url5 = "" # @param {type:"string"}
#     files = [file_url1, file_url2, file_url3, file_url4, file_url5]

files = [single_line_batch_links]  # Using the provided link

for url in files:
    if url == "":
        continue
    else:
        output_path = "download/" # @param {type:"string"}
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
            response = requests.get(final_url, stream=True)
            if response.status_code == 200:
                filename = os.path.join(output_path, download_url.split('/')[-1])
                with open(filename, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
        else:
            print("Error while fetching Katfile API")
