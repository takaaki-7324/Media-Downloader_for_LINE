from line.downloader import Download
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from oauth2client.service_account import ServiceAccountCredentials
import pytest
import os
import glob

url = "https://www.youtube.com/watch?v=4pqJA7aiVJc"
title = "@_BGM_DOVA-SYNDROME_OFFICIAL_YouTube_CHANNEL"

listurl = "https://www.youtube.com/playlist?list=PL1WbPnrCmroHOUPZGbC752p38KrQDwMBh"
title2 = "Morning_@_BGM_DOVA-SYNDROME_OFFICIAL_YouTube_CHANNEL"

media_dir = "/opt/app/tests/media/"


@pytest.fixture
def mp3():
    tag = "/mp3"
    dl = Download(url, tag, None, None)
    dl.dir = media_dir
    return dl, title


@pytest.fixture
def mov():
    tag = "/mov"
    dl = Download(url, tag, None, None)
    dl.dir = media_dir
    return dl, title


@pytest.fixture
def playlist():
    tag = "/mp3"
    dl = Download(listurl, tag, None, None)
    dl.dir = media_dir
    return dl, title, title2


@pytest.fixture
def gcp_info():
    # ファイル内容
    string = "This is upload test file."

    # 認証
    scope = "https://www.googleapis.com/auth/drive"
    json_file = glob.glob("credentials/*.json")[0]
    if os.path.isfile(json_file):
        gauth = GoogleAuth()
        gauth.credentials = ServiceAccountCredentials.from_json_keyfile_name(
            json_file, scope
        )
        auth = GoogleDrive(gauth)
        return auth, string
    else:
        print("File Not Found!")
