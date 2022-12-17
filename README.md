# Media Downloader for LINE

![python](https://img.shields.io/badge/Python-3.9+-skyblue?style=plastic&logo=python)
![docker-compose-v3](https://img.shields.io/badge/docker_compose-v3-blue?style=plastic&logo=docker)
![tool-version](https://img.shields.io/badge/tool-v1.2.0-darkred?style=plastic&logo=pastebin)

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
1. [GCP の認証情報](https://console.cloud.google.com/apis/credentials) にアクセスして「認証情報を作成」→ 「OAuthクライアントIDの作成」→　「アプリケーションの種類：デスクチップアプリ」→「名前：お好きな名前を入力」の順に進み、[作成]をクリック。</br>
OAuth 2.0 クライアントID の欄で右側の操作からダウンロードボタンをクリック。</br>
2. `client_secret.json`に名前を変更し、`./credentials`ディレクトリに設置します。</br>

3. [NGROKアカウント準備](https://dashboard.ngrok.com/get-started/setup)NGROKアカウントを作成し、Connect your accountのトークンを確認します。

4. `.env.sample` を参考に`.env`を作成します。<p>
(GoogleDriveの共有IDは `https://drive.google.com/drive/u/0/folders/` 以降の英数字を記入します。)
5. `docker-compose up --build -d `を実行しDockerを起動します。
6. 以下を実行しGoogle Auth認証を行います。※初回のみ<br>
  `docker-compose exec app python -m pip install pytest`<br>
  `docker-compose exec app pytest tests/test_upload.py`<br>
  以下が表示されたら検証コードを貼り付けてください。<br>
  `Enter verification code:` <ここに検証コードを貼り付け>
<p>

7. [NGROKのEndpointで確認](https://dashboard.ngrok.com/cloud-edge/endpoints)して、httpsから始まるURLを[LINE API](https://developers.line.biz/console/)の`Messaging API settings`に移動し、Webhook URLに記載します。<br>この時、/callbackを末尾に付けてください。<p>
  <例> `https://2aeebc8adb35.ap.ngrok.io/callback`<br>
  [Verify]をクリックして`Success`となっていればOKです。<br>
  LINEアプリから`/help` と入力してレスポンスがあれば完了です。
## 使用方法
- LINE から以下のように入力して動作します。
- /mp3 URL -- 音楽を取得できます。
- /mov URL -- 動画を取得できます。
- /nomov URL -- 動画を無変換で取得できます。