import os
import yagmail

RECIPIENT_EMAIL = "kyawkaung709@gmail.com"

def send_email(recipient_email):
    yag = yagmail.SMTP('bssgserverx@gmail.com', 'puvsaqpmhdqnjnpw')
    
    # Get the current working directory
    srt_directory = os.getcwd()
    
    # Collect all .srt and .rar files
    srt_files = [os.path.join(srt_directory, f) for f in os.listdir(srt_directory) if f.endswith('.srt')]
    rar_files = [os.path.join(srt_directory, f) for f in os.listdir(srt_directory) if f.endswith('.rar')]
    
    # Combine them into one list of attachments
    attachments = srt_files + rar_files
    
    if not attachments:
        print("No .srt or .rar files found in the current directory.")
        return

    contents = [
        "Congratulations!",
        "Your file is ready to download.",
        "Best Regards,",
        "BSSG Group"
    ]
    
    yag.send(
        to=recipient_email,
        subject="BSSG's SRT Generator",
        contents=contents,
        attachments=attachments
    )
    
    print(f"Email sent to {recipient_email} with {len(attachments)} attachments.")

if __name__ == "__main__":
    send_email(RECIPIENT_EMAIL)
