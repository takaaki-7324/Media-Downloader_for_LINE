from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

# GoogleDrive認証設定
gauth = GoogleAuth(settings_file="credentials/settings.yml")
gauth.CommandLineAuth()
drive = GoogleDrive(gauth)