import os
import shutil
from glob import glob


class TestRunner(object):

    def test_mp3_download(self, mp3):

        dl, path = mp3
        dl.downloader()
        file_exists = os.path.isfile(f"{dl.dir}{path}.m4a")
        assert file_exists

    def test_mp3_convert(self, mp3):
        dl, path = mp3
        dl.convert(f"{dl.dir}{path}.m4a")
        file_exists = os.path.isfile(f"{dl.dir}{path}.mp3")
        assert file_exists

    def test_mp3_delete(self, mp3):
        dl, path = mp3
        os.remove(f"{dl.dir}{path}.mp3")
        file_exists = os.path.isfile(f"{dl.dir}{path}.mp3")
        assert not file_exists

    def test_mov_download(self, mov):
        dl, path = mov
        dl.downloader()
        file_exists = os.path.isfile(f"{dl.dir}{path}.webm")
        assert file_exists

    def test_mov_convert(self, mov):
        dl, path = mov
        dl.convert(f"{dl.dir}{path}.webm")
        file_exists = os.path.isfile(f"{dl.dir}{path}.mp4")
        assert file_exists

    def test_mov_delete(self, mov):
        dl, path = mov
        os.remove(f"{dl.dir}{path}.mp4")
        file_exists = os.path.isfile(f"{dl.dir}{path}.mp4")
        assert not file_exists

    def test_playlist(self, playlist):
        dl, t1, t2 = playlist
        dl.downloader()
        fileExtensions = set(["mp4", "m4a", "mkv", "webm", "mp3"])
        file_list = []
        for ext in fileExtensions:
            file_list.extend(glob("%s*.%s" % (f"{dl.dir}", ext)))

        assert len(file_list) == 2
        assert t1 in str(set(file_list))
        assert t2 in str(set(file_list))

    def test_playlist_delete(self, playlist):
        dl, t1, t2 = playlist
        os.remove(f"{dl.dir}{t1}.m4a")
        os.remove(f"{dl.dir}{t2}.m4a")
        assert not os.path.isfile(f"{dl.dir}{t1}.m4a")
        assert not os.path.isfile(f"{dl.dir}{t2}.m4a")

    def test_runner(self, playlist):
        dl, _, _ = playlist
        dl.downloader()
        dl.runner()
        try:
            shutil.rmtree(f"{dl.dir}")
        except OSError:
            pass
