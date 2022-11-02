import smtplib as smtp
from email.mime.text import MIMEText
from email.header import Header


from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

from loader import MAIL_LOG, MAIL_PASS, HOST, PORT

gauth = GoogleAuth()
# Try to load saved client credentials
gauth.LoadCredentialsFile("token.json")
if gauth.credentials is None:
    # Authenticate if they're not there
    gauth.LocalWebserverAuth()
elif gauth.access_token_expired:
    # Refresh them if expired
    gauth.Refresh()
else:
    # Initialize the saved creds
    gauth.Authorize()
# Save the current credentials to a file
gauth.SaveCredentialsFile("token.json")


def upload_google(filename, filecontent):
    try:
        drive = GoogleDrive(gauth)
        file = drive.CreateFile({'title': f'{filename}'})
        file.SetContentFile(filecontent)
        file.Upload()
        permission = file.InsertPermission({
            'type': 'anyone',
            'value': 'anyone',
            'role': 'reader'})
        return file["alternateLink"]

    except Exception as ex:
        return ex


def send_to_mail(text, to):
    server = smtp.SMTP(HOST, int(PORT))
    server.starttls()
    server.login(MAIL_LOG, MAIL_PASS)
    message = f'From:{MAIL_LOG} \nSubject: Ready video from yt-merge\n\n {text}'
    server.sendmail(MAIL_LOG, to, message)
