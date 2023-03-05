# Media Downloader for LINE

![python](https://img.shields.io/badge/Python-3.9+-skyblue?style=plastic&logo=python)
![docker-compose-v3](https://img.shields.io/badge/docker_compose-v3-blue?style=plastic&logo=docker)
![tool-version](https://img.shields.io/badge/tool-v1.3.0-darkred?style=plastic&logo=pastebin)

## ツールについて
- LINEからYoutube,tiktok,soundcloud,Twitter,dailymotion,ニコニコ動画から音楽・動画のダウンロードに対応しています。<p>
- ダウンロード後は自動的に、変換→GoogleDriveにアップロード→LINEに完了通知を行います。
- Youtubeのプレイリストにも対応しています。
- 複数の音楽・動画の同時変換に対応し、GoogleDriveへの同時アップロードが行えます。(デフォルト8つ同時処理)

## 前提条件
- [LINE API](https://developers.line.biz/console/)を取得してください。
- [GoogleDriveAPI](https://console.developers.google.com/apis/library/drive.googleapis.com)を有効にします。
- docker-composeを準備してください。
- [NGROKアカウント準備](https://dashboard.ngrok.com/get-started/setup)NGROKアカウントを作成してください。
<p>

## 準備
1. [GCP の認証情報](https://console.cloud.google.com/apis/credentials) にアクセスしてサービスアカウントを作成(省略可は省略する)。のメールアドレスをクリック → 「キー」タブに移動 →　「鍵を追加」→「新しい鍵を作成」→ 「JSONタイプ」→「作成」でJSONファイルがダウンロードされるので、そのまま`Media-Downloader_for_LINE/credentials`のフォルダ以下に設置。<br />
※ サービスアカウントのメールアドレスは後で使用しますので、控えておいてください。<br />

2. [NGROKアカウント準備](https://dashboard.ngrok.com/get-started/setup)NGROKアカウントを作成し、Connect your accountのトークンを確認します。

3. Google DriveでMUSIC用、VIDEO用に2つフォルダを作成します。<br />
<b />※ この時作成したフォルダを共有する相手は先ほどのサービスアカウントのメールアドレスを追加します。<br />
　 フォルダの権限は「編集者」、一般的なアクセスは「制限付き」でOKです。

4. `.env.sample` を参考に`.env`を作成します。<p>
(GoogleDriveの共有IDは `https://drive.google.com/drive/u/0/folders/` 以降の英数字を記入します。)


5. `docker-compose up --build -d `を実行しDockerを起動します。

6. [NGROKのEndpointで確認](https://dashboard.ngrok.com/cloud-edge/endpoints)して、httpsから始まるURLを[LINE API](https://developers.line.biz/console/)の`Messaging API settings`に移動し、Webhook URLに記載します。<br>この時、/callbackを末尾に付けてください。<p>
  <例> `https://2aeebc8adb35.ap.ngrok.io/callback`<br>
  [Verify]をクリックして`Success`となっていればOKです。<br>
  LINEアプリから`/help` と入力してレスポンスがあれば完了です。
## 使用方法
- LINE から以下のように入力して動作します。
- /mp3 URL -- 音楽を取得できます。
- /mov URL -- 動画を取得できます。
- /nomov URL -- 動画を無変換で取得できます。

## GoogleDriveへのアップロードを確認する場合
以下コマンドを実行します。
- `dokcer-compose exec app python -m pip install pytest`
- `docker-compose exec app pytest tests/test_upload.py`

以下項目を確認します。
- 指定したフォルダに「UPLOAD_TEST_FILE.txt」と書かれたファイルがアップロードされている。
- `This is upload test file.` の文字列が記載されている。