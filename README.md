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
- docker-composeを準備してください。<p>
## 準備
- [GCP の認証情報](https://console.cloud.google.com/apis/credentials) にアクセスして「認証情報を作成」→ 「OAuthクライアントIDの作成」→　「アプリケーションの種類：デスクチップアプリ」→「名前：お好きな名前を入力」の順に進み、[作成]をクリック。</br>
OAuth 2.0 クライアントID の欄で右側の操作からダウンロードボタンをクリック。</br>
- `client_secrets.json`に名前を変更し、`credentials`ディレクトリに設置します。</br>

- `.env.sample` を参考に`.env`を作成します。<p>
(GoogleDriveの共有IDは `https://drive.google.com/drive/u/0/folders/` 以降の英数字を記入します。)
- `docker-compose up --build`を実行して認証情報の設定を行います。
- 認証後は Ctrl + C で一旦停止し、`docker-compose up -d` で起動します。<p>
- http://localhost:4040 にアクセスして、httpsから始まるURLを[LINE API](https://developers.line.biz/console/)の`Messaging API settings`に移動し、Webhook URLに記載します。この時、/callbackを末尾に付けてください。<p>
  <例> `https://2aeebc8adb35.ap.ngrok.io/callback`
- [Verify]をクリックして`Success`となっていればOKです。
- LINEアプリから`/help` と入力してレスポンスがあれば完了です。
## 使用方法
- LINE から以下のように入力して動作します。
- /mp3 URL -- 音楽を取得できます。
- /mov URL -- 動画を取得できます。
- /nomov URL -- 動画を無変換で取得できます。