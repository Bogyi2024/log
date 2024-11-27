import os
import yagmail

RECIPIENT_EMAIL = "soemyatoo13@gmail.com"

def send_email(recipient_email):
    yag = yagmail.SMTP('bssgserverx@gmail.com', 'puvsaqpmhdqnjnpw')
    
    # Get the current working directory
    srt_directory = os.getcwd()
    
    # List all .srt files in the directory
    srt_files = [os.path.join(srt_directory, file) for file in os.listdir(srt_directory) if file.endswith('.srt')]
    
    if not srt_files:
        print("No .srt files found in the current directory.")
        return

    contents = [
        "Congratulation!",
        "Your file is ready to download.",
        "Best Regards,",
        "BSSG Group"
    ]
    
    yag.send(to=recipient_email, subject="BSSG's srt Generator", contents=contents, attachments=srt_files)
    print(f"Email sent to {recipient_email} with {len(srt_files)} attachments.")

if __name__ == "__main__":
    send_email(RECIPIENT_EMAIL)
