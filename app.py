#!/bin/env python
import setting as s
import re
import os
from line.downloader import Download
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent,TextMessage,TextSendMessage
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

# アプリケーションフレームワーク
app = Flask(__name__)

# LINE チャンネルシークレット
LINE_CHANNEL_SECRET = s.LINE_CHANNEL_SECRET
# LINE アクセストークン
LINE_CHANNEL_ACCESS_TOKEN = s.LINE_CHANNEL_ACCESS_TOKEN

# GoogleDrive共有フォルダID
MUSIC_FOLDER_ID = s.MUSIC_FOLDER_ID
VIDEO_FOLDER_ID = s.VIDEO_FOLDER_ID

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

@app.route("/callback", methods=['POST'])
def callback():
    # X-Line-Signature シグネチャの取得
    signature = request.headers['X-Line-Signature']

    # 内容の取得
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # ウェブフックの確立
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=(TextMessage))
def line(event):
    # LINEメッセージイベント
    message = event.message.text
    if message.startswith("/help"):
        msg = TextSendMessage(
            text=(
                "/mp3 -- 音楽をダウンロードします\n"
                "/mov -- 動画をダウンロードします\n"
                "/nomov -- 無変換でダウンロードします\n"
                )
            )
        line_bot_api.reply_message(event.reply_token,msg)

    elif message.startswith("/"):

        param = set(["/mp3","/mov","/nomov"])

        try:
            tag,url = message.split()
        except ValueError:
            pattern = r"https?://[\w/:%#\$&\?\(\)~\.=\+\-]+"
            if not re.match(pattern, url):
                msg = TextSendMessage(text="URLが指定されていません！")
                line_bot_api.reply_message(event.reply_token,msg)
        else:
            if tag in str(param):
                if tag == "/mp3":
                    FOLDER = MUSIC_FOLDER_ID
                else:
                    FOLDER = VIDEO_FOLDER_ID

                try:
                    lineid = event.source.group_id
                except AttributeError:
                    lineid = event.source.user_id

                dl = Download(url,tag,line_bot_api,lineid)
                try:
                    dl.downloader()
                except Exception as e:
                    msg = TextSendMessage(text=f"エラーが発生しました。\n{e.args[0]}")
                    line_bot_api.reply_message(event.reply_token,msg)
                else:
                    msg = TextSendMessage(text=(
                        "ダウンロード完了しました。変換処理実行中です。\n"
                        f"完了後、以下に保存されます。\nhttps://drive.google.com/drive/u/0/folders/{FOLDER}"
                        )
                    )
                    line_bot_api.reply_message(event.reply_token,msg)
                    dl.Runner()

if __name__ == "__main__":
    if os.path.isfile("credentials/credentials.json"):
        app.run(host="0.0.0.0", port=9000)
    else:
        # GoogleDrive認証設定
        gauth = GoogleAuth(settings_file="credentials/settings.yml")
        gauth.CommandLineAuth()
        drive = GoogleDrive(gauth)