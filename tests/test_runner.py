import os

class TestRunner(object):

    def test_mp3_download(self,mp3):

        dl,path = mp3
        dl.downloader()
        file_exists= os.path.isfile(f"./{path}.m4a")
        assert file_exists

    def test_mp3_convert(self,mp3):
        dl,path = mp3
        dl.convert(f"./{path}.m4a")
        file_exists= os.path.isfile(f"./{path}.mp3")
        assert file_exists

    def test_mp3_delete(self,mp3):
        _,path = mp3
        os.remove(f"./{path}.mp3")
        file_exists= os.path.isfile(f"./{path}.mp3")
        assert not file_exists

    def test_mov_download(self,mov):
        dl,path = mov
        dl.downloader()
        file_exists= os.path.isfile(f"./{path}.webm")
        assert file_exists

    def test_mov_convert(self,mov):
        dl,path = mov
        dl.convert(f"./{path}.webm")
        file_exists= os.path.isfile(f"./{path}.mp4")
        assert file_exists

    def test_mov_delete(self,mov):
        _,path = mov
        os.remove(f"./{path}.mp4")
        file_exists= os.path.isfile(f"./{path}.mp4")
        assert not file_exists