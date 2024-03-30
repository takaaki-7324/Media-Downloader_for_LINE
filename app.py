#!/bin/env python
import setting as s
import re
from line.downloader import Download
from flask import Flask, request, abort
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage,
)
from linebot.v3.webhooks import MessageEvent, TextMessageContent

# アプリケーションフレームワーク
app = Flask(__name__)

# LINE チャンネルシークレット
LINE_CHANNEL_SECRET = s.LINE_CHANNEL_SECRET
# LINE アクセストークン
LINE_CHANNEL_ACCESS_TOKEN = s.LINE_CHANNEL_ACCESS_TOKEN

# GoogleDrive共有フォルダID
MUSIC_FOLDER_ID = s.MUSIC_FOLDER_ID
VIDEO_FOLDER_ID = s.VIDEO_FOLDER_ID

# APIインスタンス化
configuration = Configuration(access_token=LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)


@app.route("/callback", methods=["POST"])
def callback():
    # X-Line-Signature シグネチャの取得
    signature = request.headers["X-Line-Signature"]

    # 内容の取得
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # ウェブフックの確立
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return "OK"


@handler.add(MessageEvent, message=TextMessageContent)
def line(event):

    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)

    # LINEメッセージイベント
    message = event.message.text
    if message.startswith("/help"):
        help_message = (
            "/mp3 -- 音楽をダウンロードします\n"
            "/mov -- 動画をダウンロードします\n"
            "/nomov -- 無変換でダウンロードします\n"
        )
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token, messages=[TextMessage(text=help_message)]
            )
        )

    elif message.startswith("/"):

        param = set(["/mp3", "/mov", "/nomov"])

        try:
            tag, url = message.split()
        except ValueError:
            pattern = r"https?://[\w/:%#\$&\?\(\)~\.=\+\-]+"
            if not re.match(pattern, url):
                error_message = "URLが指定されていません！"
                line_bot_api.reply_message_with_http_info(
                    ReplyMessageRequest(
                        reply_token=event.reply_token,
                        messages=[TextMessage(text=error_message)],
                    )
                )
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

                dl = Download(url, tag, line_bot_api, lineid)
                try:
                    dl.downloader()
                except Exception as e:
                    error_message = f"エラーが発生しました。\n{e.args[0]}"
                    line_bot_api.reply_message_with_http_info(
                        ReplyMessageRequest(
                            reply_token=event.reply_token,
                            messages=[TextMessage(text=error_message)],
                        )
                    )
                else:
                    complete_message = (
                        "ダウンロード完了しました。変換処理実行中です。\n"
                        f"完了後、以下に保存されます。\nhttps://drive.google.com/drive/u/0/folders/{FOLDER}"
                    )
                    line_bot_api.reply_message_with_http_info(
                        ReplyMessageRequest(
                            reply_token=event.reply_token,
                            messages=[TextMessage(text=complete_message)],
                        )
                    )
                    dl.runner()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9000)
