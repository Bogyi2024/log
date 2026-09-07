import os
import gdown
import subprocess
import re
import mediafire_dl


def extract_google_drive_id(url):
    """Extract a Google Drive file or folder ID."""
    pattern = re.compile(
        r"drive.google.com/.*?(?:file/d/|drive/folders/|open\?id=|uc\?id=)([^/&?]+)"
    )
    match = pattern.search(url)
    return match.group(1) if match else None


links_content = os.getenv("LINKS_CONTENT")

if links_content:
    links = links_content.splitlines()
    print(f"Loaded {len(links)} links from environment variable.")
else:
    print("Error: LINKS_CONTENT environment variable not found or is empty.")
    links = []

if links:
    output_path = "source/"
    os.makedirs(output_path, exist_ok=True)
    current_dir = os.getcwd()

    for raw_url in links:
        url = raw_url.strip()
        if not url:
            continue

        print(f"\n--- Processing URL: {url} ---")
        file_id = extract_google_drive_id(url)

        if file_id:
            try:
                print(f"Attempting download via gdown (file ID): {file_id}")
                gdown.download(id=file_id, output=output_path, quiet=False)
                print(f"Successfully downloaded file with ID: {file_id}")
            except Exception as error:
                print(f"gdown file download failed ({error}). Attempting as folder...")
                try:
                    gdown.download_folder(
                        id=file_id, output=output_path, quiet=False, resume=True
                    )
                    print(f"Successfully downloaded folder with ID: {file_id}")
                except Exception as folder_error:
                    print(
                        f"Error downloading {file_id} as file and folder: "
                        f"{folder_error}"
                    )

        elif "msubb2.net" in url:
            print(f"Attempting download via wget: {url}")
            try:
                subprocess.run(["wget", "-P", output_path, url], check=True)
                print("Successfully downloaded msubb2.net link.")
            except FileNotFoundError:
                print("Error: wget is not installed or not in PATH.")
            except subprocess.CalledProcessError as error:
                print(f"wget download failed (exit code {error.returncode}).")
            except Exception as error:
                print(f"Unexpected wget error: {error}")

        elif "workers" in url:
            print(f"Attempting download via curl: {url}")
            try:
                os.chdir(output_path)
                subprocess.run(["curl", "-O", "-J", url], check=True)
                print("Successfully downloaded workers link.")
            except FileNotFoundError:
                print("Error: curl is not installed or not in PATH.")
            except subprocess.CalledProcessError as error:
                print(f"curl download failed (exit code {error.returncode}).")
            except Exception as error:
                print(f"Unexpected curl error: {error}")
            finally:
                os.chdir(current_dir)

        elif url.startswith("https://download") or "mediafire.com" in url:
            try:
                os.chdir(output_path)
                if url.startswith("https://download"):
                    parts = url.split("/")
                    if len(parts) >= 6:
                        mediafire_url = (
                            f"https://www.mediafire.com/file/{parts[-2]}/{parts[-1]}"
                        )
                        mediafire_dl.download(mediafire_url, quiet=False)
                    else:
                        print("MediaFire raw link format not recognized.")
                else:
                    mediafire_dl.download(url, quiet=False)
                print(f"Downloaded: {url}")
            except Exception as error:
                print(f"Error downloading from MediaFire: {error}")
            finally:
                os.chdir(current_dir)

        else:
            # Safer generic downloader settings: 2 connections instead of 16.
            filename = url.split("/")[-1].split("?")[0]
            if not filename or "." not in filename:
                filename = "unknown_download"

            print(f"Attempting download via aria2c with 2 connections: {filename}")
            try:
                subprocess.run(
                    [
                        "./aria2c",
                        "-c",
                        "-d", output_path,
                        "-o", filename,
                        "-x", "2",
                        "-s", "2",
                        "--max-connection-per-server=2",
                        "--retry-wait=15",
                        "--max-tries=5",
                        "--timeout=60",
                        "--connect-timeout=30",
                        url,
                    ],
                    check=True,
                )
                print(f"Downloaded: {os.path.join(output_path, filename)}")
            except subprocess.CalledProcessError as error:
                print(
                    f"aria2c download failed (exit code {error.returncode}). "
                    "Try a fresh generated link after waiting a few minutes."
                )
            except FileNotFoundError:
                print("Error: ./aria2c was not found in the working directory.")
            except Exception as error:
                print(f"Error downloading {url} via aria2c: {error}")
else:
    print("No links found in the links content.")

print("\nDownload script finished.")
