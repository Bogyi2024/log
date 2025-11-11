import os
import base64
import yagmail
from huggingface_hub import HfApi
import urllib.parse

RECIPIENT_EMAIL = os.getenv('RECEIPT_EMAIL')

# Base64-encoded Hugging Face token
HF_TOKEN_B64 = "aGZfUVJLalVWWXFCZGxNSW9Ed3dYT1lmdk1kam5FbUVncE12TA=="

# Decode token from base64
HF_TOKEN = base64.b64decode(HF_TOKEN_B64).decode("utf-8")

HF_REPO = "bigbossmonster/bssg"

# Initialize API with token
api = HfApi(token=HF_TOKEN)


def upload_to_hf(file_path):
    filename = os.path.basename(file_path)
    api.upload_file(
        path_or_fileobj=file_path,
        path_in_repo=filename,
        repo_id=HF_REPO,
        repo_type="dataset",
        token=HF_TOKEN,
    )
    # Encode filename for safe URL
    filename_encoded = urllib.parse.quote(filename)
    return f"https://huggingface.co/datasets/{HF_REPO}/blob/main/{filename_encoded}"


def send_email(recipient_email):
    yag = yagmail.SMTP("bssgserverx@gmail.com", "puvsaqpmhdqnjnpw")

    srt_directory = os.getcwd()

    srt_files = [
        os.path.join(srt_directory, f)
        for f in os.listdir(srt_directory)
        if f.endswith(".srt")
    ]
    rar_files = [
        os.path.join(srt_directory, f)
        for f in os.listdir(srt_directory)
        if f.endswith(".rar")
    ]

    rar_links = [f"{os.path.basename(r)}: {upload_to_hf(r)}" for r in rar_files]

    if not srt_files and not rar_links:
        print("No .srt or .rar files found in the current directory.")
        return

    contents = [
        "Congratulations!",
        "Your file is ready to download.",
    ]

    if srt_files:
        contents.append("Attached: " + ", ".join(os.path.basename(f) for f in srt_files))

    if rar_links:
        contents.append("RAR files were uploaded to Hugging Face:")
        contents.append("\n".join(rar_links))

    contents.extend(
        [
            "Best Regards,",
            "BSSG Group",
        ]
    )

    yag.send(
        to=recipient_email,
        subject="BSSG's SRT Generator",
        contents=contents,
        attachments=srt_files if srt_files else None,
    )

    print(
        f"Email sent to {recipient_email}. {len(srt_files)} srt attached, {len(rar_links)} rar links."
    )


if __name__ == "__main__":
    send_email(RECIPIENT_EMAIL)
