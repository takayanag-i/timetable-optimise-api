# Cloud Run デプロイ手順（Cloud Buildトリガー）

このドキュメントでは、GitHubからCloud Buildトリガーを使用してGoogle Cloud Runにデプロイする手順を説明します。

## 前提条件

1. Google Cloud SDK (gcloud) がインストールされていること
2. GitHubリポジトリが作成されていること
3. Google Cloudプロジェクトが作成されていること
4. 必要な権限（Cloud Run Admin、Cloud Build Editor等）があること
5. Gurobiライセンス情報（WLSACCESSID、WLSSECRET、LICENSEID）があること

## 事前準備

### 1. gcloud認証とプロジェクト設定

```bash
# Google Cloudにログイン
gcloud auth login

# プロジェクトを設定
gcloud config set project YOUR_PROJECT_ID

# アプリケーションのデフォルト認証情報を設定
gcloud auth application-default login
```

### 2. 必要なAPIの有効化

```bash
PROJECT_ID="your-project-id"

# Cloud Run API
gcloud services enable run.googleapis.com

# Cloud Build API
gcloud services enable cloudbuild.googleapis.com

# Container Registry API（一時的なイメージ保存用）
gcloud services enable containerregistry.googleapis.com
```

### 3. Cloud Buildサービスアカウントに権限を付与

```bash
PROJECT_ID="your-project-id"
PROJECT_NUMBER=$(gcloud projects describe $PROJECT_ID --format="value(projectNumber)")

# Cloud Run Admin権限を付与
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:${PROJECT_NUMBER}@cloudbuild.gserviceaccount.com" \
    --role="roles/run.admin"

# Service Account User権限を付与
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:${PROJECT_NUMBER}@cloudbuild.gserviceaccount.com" \
    --role="roles/iam.serviceAccountUser"
```

### 4. 環境変数の設定（Secret Managerを使用 - 推奨）

```bash
PROJECT_ID="your-project-id"

# Secretを作成
echo -n "your-wlsaccessid" | gcloud secrets create wlsaccessid --data-file=-
echo -n "your-wlssecret" | gcloud secrets create wlssecret --data-file=-
echo -n "your-licenseid" | gcloud secrets create licenseid --data-file=-

# Cloud BuildサービスアカウントにSecretへのアクセス権限を付与
PROJECT_NUMBER=$(gcloud projects describe $PROJECT_ID --format="value(projectNumber)")
gcloud secrets add-iam-policy-binding wlsaccessid \
    --member="serviceAccount:${PROJECT_NUMBER}@cloudbuild.gserviceaccount.com" \
    --role="roles/secretmanager.secretAccessor"
gcloud secrets add-iam-policy-binding wlssecret \
    --member="serviceAccount:${PROJECT_NUMBER}@cloudbuild.gserviceaccount.com" \
    --role="roles/secretmanager.secretAccessor"
gcloud secrets add-iam-policy-binding licenseid \
    --member="serviceAccount:${PROJECT_NUMBER}@cloudbuild.gserviceaccount.com" \
    --role="roles/secretmanager.secretAccessor"
```

## Cloud Buildトリガーの設定

### 方法1: gcloudコマンドで設定

```bash
PROJECT_ID="your-project-id"
REPO_NAME="your-repo-name"
REPO_OWNER="your-github-username"
REGION="asia-northeast1"

# GitHub接続を作成（初回のみ）
gcloud builds triggers create github \
    --name="deploy-timetable-api" \
    --repo-name="$REPO_NAME" \
    --repo-owner="$REPO_OWNER" \
    --branch-pattern="^main$" \
    --build-config="cloudbuild-github.yaml" \
    --region="$REGION"
```

### 方法2: Cloud Consoleから設定（推奨）

1. [Cloud Console](https://console.cloud.google.com/cloud-build/triggers) にアクセス
2. 「トリガーを接続」をクリック
3. GitHubを選択し、認証を行う
4. リポジトリを選択
5. トリガー設定：
   - **名前**: `deploy-timetable-api`
   - **イベント**: プッシュ
   - **ブランチ**: `^main$`
   - **設定タイプ**: クラウドビルド設定ファイル（yaml または json）
   - **場所**: `cloudbuild-github.yaml`
   - **変数**: 以下の環境変数を設定
     - `_WLSACCESSID`: Secret Managerから取得するか、直接値を設定
     - `_WLSSECRET`: Secret Managerから取得するか、直接値を設定
     - `_LICENSEID`: Secret Managerから取得するか、直接値を設定

### cloudbuild-github.yamlの設定確認

`cloudbuild-github.yaml` ファイルが正しく設定されているか確認してください。必要に応じて、以下の設定を調整できます：

- `_REGION`: デプロイ先のリージョン（デフォルト: `asia-northeast1`）
- `_SERVICE_NAME`: Cloud Runサービス名（デフォルト: `timetable-api`）
- `_MEMORY`: メモリサイズ（デフォルト: `2Gi`）
- `_CPU`: CPU数（デフォルト: `2`）
- `_TIMEOUT`: タイムアウト（秒）（デフォルト: `3600`）
- `_MAX_INSTANCES`: 最大インスタンス数（デフォルト: `10`）

### Secret Managerから環境変数を読み込む場合

`cloudbuild-github.yaml` のsubstitutionsセクションを以下のように更新：

```yaml
substitutions:
  _REGION: 'asia-northeast1'
  _SERVICE_NAME: 'timetable-api'
  _MEMORY: '2Gi'
  _CPU: '2'
  _TIMEOUT: '3600'
  _MAX_INSTANCES: '10'
  _WLSACCESSID: '$(gcloud secrets versions access latest --secret=wlsaccessid)'
  _WLSSECRET: '$(gcloud secrets versions access latest --secret=wlssecret)'
  _LICENSEID: '$(gcloud secrets versions access latest --secret=licenseid)'
```

または、Cloud Buildトリガーの設定画面で環境変数を直接指定することも可能です。

## デプロイの実行

GitHubのmainブランチにプッシュすると、自動的にデプロイが開始されます：

```bash
git add .
git commit -m "Deploy to Cloud Run"
git push origin main
```

## デプロイの確認

### Cloud Buildの履歴を確認

```bash
# 最新5件のビルド履歴を確認
gcloud builds list --limit=5

# 最新のビルドIDを取得
BUILD_ID=$(gcloud builds list --limit=1 --format="value(id)")

# ビルドログを確認
gcloud builds log $BUILD_ID
```

### Cloud Runサービスの状態を確認

```bash
SERVICE_NAME="timetable-api"
REGION="asia-northeast1"

# サービスの詳細を確認
gcloud run services describe $SERVICE_NAME --region $REGION

# サービスURLを取得
gcloud run services describe $SERVICE_NAME --region $REGION --format="value(status.url)"
```

### ヘルスチェック

```bash
SERVICE_URL=$(gcloud run services describe timetable-api --region asia-northeast1 --format="value(status.url)")
curl $SERVICE_URL/docs
```

### ログの確認

```bash
gcloud run services logs read timetable-api --region asia-northeast1
```

## 環境変数の更新

Cloud Runサービスに環境変数を更新するには：

```bash
gcloud run services update timetable-api \
    --region asia-northeast1 \
    --update-env-vars "WLSACCESSID=your-wlsaccessid,WLSSECRET=your-wlssecret,LICENSEID=your-licenseid,CBC_PATH=/usr/bin/cbc"
```

### Secret Managerを使用する場合（推奨）

より安全に環境変数を管理するには、Secret Managerを使用します：

```bash
# Secretを更新
echo -n "new-wlsaccessid" | gcloud secrets versions add wlsaccessid --data-file=-
echo -n "new-wlssecret" | gcloud secrets versions add wlssecret --data-file=-
echo -n "new-licenseid" | gcloud secrets versions add licenseid --data-file=-

# Cloud RunサービスにSecretをマウント
gcloud run services update timetable-api \
    --region asia-northeast1 \
    --update-secrets WLSACCESSID=wlsaccessid:latest,WLSSECRET=wlssecret:latest,LICENSEID=licenseid:latest
```

## リソース設定

デフォルトのリソース設定：
- **メモリ**: 2Gi
- **CPU**: 2
- **タイムアウト**: 3600秒（1時間）
- **最大インスタンス数**: 10

必要に応じて調整：

```bash
gcloud run services update timetable-api \
    --region asia-northeast1 \
    --memory 4Gi \
    --cpu 4 \
    --timeout 7200 \
    --max-instances 20
```

または、`cloudbuild-github.yaml` のsubstitutionsを更新して、次回のデプロイ時に反映させます。

## トラブルシューティング

### 1. ビルドエラー

- Dockerfileの構文を確認
- 依存関係が正しくインストールされているか確認
- Cloud Buildのログを確認: `gcloud builds log BUILD_ID`

### 2. 起動エラー

- 環境変数が正しく設定されているか確認
- ポート設定（Cloud RunはPORT環境変数を使用）を確認
- ログを確認: `gcloud run services logs read timetable-api --region asia-northeast1`

### 3. Gurobiライセンスエラー

- WLSACCESSID、WLSSECRET、LICENSEIDが正しく設定されているか確認
- Gurobiライセンスが有効であることを確認
- ネットワーク接続を確認（Webライセンスサーバーを使用する場合）

### 4. CBCソルバーエラー

- CBC_PATH環境変数が正しく設定されているか確認（デフォルト: /usr/bin/cbc）
- CBCが正しくインストールされているか確認

### 5. 権限エラー

- Cloud Buildサービスアカウントに適切な権限が付与されているか確認
- IAMポリシーを確認: `gcloud projects get-iam-policy $PROJECT_ID`

### 6. デプロイタイムアウト

- ビルド時間が長い場合は、Cloud Buildのタイムアウト設定を調整
- `cloudbuild-github.yaml` の `machineType` を変更: `machineType: 'E2_HIGHCPU_8'`

### 7. トリガーが動作しない

- GitHub接続が正しく設定されているか確認
- ブランチパターンが正しいか確認（`^main$`）
- トリガーの状態を確認: `gcloud builds triggers list`

## ローカルでのテスト

デプロイ前にローカルでDockerイメージをテスト：

```bash
# イメージをビルド
docker build -t timetable-api:local .

# 環境変数を設定して実行
docker run -p 8080:8080 \
    -e WLSACCESSID="your-wlsaccessid" \
    -e WLSSECRET="your-wlssecret" \
    -e LICENSEID="your-licenseid" \
    -e CBC_PATH="/usr/bin/cbc" \
    timetable-api:local

# ブラウザで http://localhost:8080/docs にアクセス
```

## 更新デプロイ

コードを更新した後、mainブランチにプッシュするだけで自動的にデプロイが開始されます：

```bash
git add .
git commit -m "Update application"
git push origin main
```

## トリガーの管理

### トリガー一覧の確認

```bash
gcloud builds triggers list
```

### トリガーの削除

```bash
gcloud builds triggers delete TRIGGER_ID
```

### トリガーの更新

```bash
gcloud builds triggers update TRIGGER_ID \
    --branch-pattern="^main$|^develop$"
```

## 参考リンク

- [Cloud Run ドキュメント](https://cloud.google.com/run/docs)
- [Cloud Build ドキュメント](https://cloud.google.com/build/docs)
- [Cloud Build トリガー](https://cloud.google.com/build/docs/triggers)
- [Gurobi ドキュメント](https://www.gurobi.com/documentation/)
- [CBC ソルバー](https://github.com/coin-or/Cbc)
