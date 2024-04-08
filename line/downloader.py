#!/bin/env python3
from yt_dlp import YoutubeDL
from glob import glob
from line.uploader import uploader
import os


class Download(object):
    def __init__(self, url, tag, lineapi, lineid):
        # ダウンロードURL
        self.url = url

        # ダウンロード一時保存先
        self.dir = "/temp/"

        # 並列処理に使用するプロセス数
        self.maxworker = 8

        # フォーマットタグ
        self.tag = tag

        # LINE API
        self.lineapi = lineapi

        # LINE ROOM ID
        self.lineid = lineid

    # ダウンロードを行う
    def downloader(self):
        fmt = {
            "/mp3": {
                "format": "m4a/bestaudio/best",
                "postprocessors": [
                    {  # Extract audio using ffmpeg
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "m4a",
                    }
                ],
            },
            "/mov": {"format": "bv[ext=webm]+ba[ext=webm]"},
        }
        opt = fmt.get(self.tag, {})

        option = {
            "outtmpl": f"{self.dir}%(title)s.%(ext)s",
            "restrictfilenames": "True",
            "quiet": "True",
            "no_warnings": "True",
            "default_search": "error",
        }
        # フォーマット形成
        option.update(opt)

        with YoutubeDL(option) as ydl:
            ydl.download([self.url])

    # 変換実行処理
    def runner(self):
        fileExtensions = set(["mp4", "m4a", "mkv", "webm", "mp3"])
        file_list = []
        for ext in fileExtensions:
            file_list.extend(glob(f"{self.dir}*.{ext}"))
        for file in file_list:
            self.convert(file)

    #     loop = asyncio.new_event_loop()
    #     loop.run_until_complete(self.multi_convert(loop, file_list))

    # # 並列処理
    # async def multi_convert(self, loop, file_list):
    #     executor = ProcessPoolExecutor()
    #     queue = asyncio.Queue()
    #     [queue.put_nowait(files) for files in file_list]
    #     print("Async")

    #     async def proc(q):
    #         while not q.empty():
    #             data = await q.get()
    #             future = loop.run_in_executor(executor, self.convert, data)
    #             await future

    #     tasks = [asyncio.create_task(proc(queue)) for _ in range(self.maxworker)]
    #     return await asyncio.wait(tasks)

    # 統合変換処理部分
    def convert(self, file):
        ext_dict = {
            ".m4a": ['ffmpeg -y -i "%s" -ab 256k "%s" -loglevel quiet', "/mp3"],
            ".mp4": ['ffmpeg -y -i "%s" -ab 256k "%s" -loglevel quiet', "/mp3"],
            ".webm": ['ffmpeg -y -i "%s" "%s" -loglevel quiet', "/mov"],
            ".mkv": ['ffmpeg -y -i "%s" -vcodec copy "%s" -loglevel quiet', "/mov"],
        }
        root, ext = os.path.splitext(file)
        formats = ext_dict.get(ext)
        if formats != None and formats[1] == self.tag:
            if ext != ".mp4" and self.tag == "/mov":
                cnv_mp4 = "%s.mp4" % root
                file = cnv_mp4
                cmd = formats[0] % (root + ext, cnv_mp4)
                os.system(cmd)
                os.remove(root + ext)
            else:
                cnv_mp3 = "%s.mp3" % root
                file = cnv_mp3
                cmd = formats[0] % (root + ext, cnv_mp3)
                os.system(cmd)
                os.remove(root + ext)

        if self.lineapi:
            uploader(self.tag, file, self.dir, self.lineapi, self.lineid)
