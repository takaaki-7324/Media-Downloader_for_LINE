import setting as s
import math
import os
from mutagen.mp3 import MP3
from line.messenger import push_message
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

# GoogleDrive共有フォルダID
MUSIC_FOLDER_ID = s.MUSIC_FOLDER_ID
VIDEO_FOLDER_ID = s.VIDEO_FOLDER_ID

# コンテンツ
def uploader(tag,data,dir,lineapi,lineid):

    gauth = GoogleAuth(settings_file="credentials/settings.yml")
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)

    video_ext_dicts = {
        '.mp4':'video/mp4',
        '.webm':'video/webm',
        '.mkv':'video/x-matroska'
    }
    title = data.lstrip(dir)
    if tag == "/mp3":
        f = drive.CreateFile(
            {
            'title': title,
            'mimeType': 'audio/mpeg',
            'parents': 
                [{'kind': 'drive#fileLink', 'id':MUSIC_FOLDER_ID}]
            }
        )
        file_length = MP3(data).info.length
        dur = math.floor(file_length * 1000)
    else:
        dur = None
        _, ext = os.path.splitext(data)
        mimeType = video_ext_dicts.get(ext)

        f = drive.CreateFile(
            {
            'title': title,
            'mimeType': mimeType,
            'parents': 
                [{'kind': 'drive#fileLink', 'id':VIDEO_FOLDER_ID}]
            }
        )

    f.SetContentFile(dir + f['title'])
    # GoogleDriveにアップロード
    f.Upload()

    # # GoogleDriveのファイルIDを取得
    file_id = drive.ListFile(
        {'q': 'title =\"' + title +  '\"'}
    ).GetList()[0]['id']
    
    link = f"https://drive.google.com/uc?export=view&id={file_id}"
    push_message(link,lineid,tag,title,dur,lineapi)
    os.remove(data)