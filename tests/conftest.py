from line.downloader import Download
import pytest


url = "https://www.youtube.com/watch?v=4pqJA7aiVJc"
title = "@_BGM_DOVA-SYNDROME_OFFICIAL_YouTube_CHANNEL"

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