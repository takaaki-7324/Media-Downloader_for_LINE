from line.downloader import Download
import pytest


url = "https://www.youtube.com/watch?v=4pqJA7aiVJc"
title = "@_BGM_DOVA-SYNDROME_OFFICIAL_YouTube_CHANNEL"

listurl = "https://www.youtube.com/playlist?list=PL1WbPnrCmroHOUPZGbC752p38KrQDwMBh"
title2 = "Morning_@_BGM_DOVA-SYNDROME_OFFICIAL_YouTube_CHANNEL"

@pytest.fixture
def mp3():
    tag = "/mp3"
    dl = Download(url,tag,None,None)
    dl.dir = "./"
    return dl,title

@pytest.fixture
def mov():
    tag = "/mov"
    dl = Download(url,tag,None,None)
    dl.dir = "./"
    return dl,title

@pytest.fixture
def playlist():
    tag = "/mp3"
    dl = Download(listurl,tag,None,None)
    dl.dir = "./"
    return dl,title,title2