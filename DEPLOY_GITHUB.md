# GitHubから直接Cloud Runにデプロイする方法

このドキュメントでは、Artifact Registryを経由せずにGitHubから直接Cloud Runにデプロイする方法を説明します。

## 方法1: Cloud Buildトリガーを使用（推奨）

GitHubへのプッシュをトリガーに自動デプロイする方法です。

### 前提条件

1. Google Cloud SDK (gcloud) がインストールされていること
2. GitHubリポジトリが作成されていること
3. Google Cloudプロジェクトが作成されていること
4. 必要な権限（Cloud Run Admin、Cloud Build Editor等）があること

### セットアップ手順

#### 1. 必要なAPIの有効化

```bash
# Cloud Run API
gcloud services enable run.googleapis.com

# Cloud Build API
gcloud services enable cloudbuild.googleapis.com

# Container Registry API（一時的なイメージ保存用）
gcloud services enable containerregistry.googleapis.com
```

#### 2. Cloud Buildサービスアカウントに権限を付与

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

#### 3. GitHubリポジトリとの接続

```bash
# GitHub接続を作成（初回のみ）
gcloud builds triggers create github \
    --name="deploy-timetable-api" \
    --repo-name="your-repo-name" \
    --repo-owner="your-github-username" \
    --branch-pattern="^main$" \
    --build-config="cloudbuild-github.yaml" \
    --region="asia-northeast1"
```

または、GitHub UIから接続：
1. [Cloud Console](https://console.cloud.google.com/cloud-build/triggers) にアクセス
2. 「トリガーを接続」をクリック
3. GitHubを選択し、認証を行う
4. リポジトリを選択
5. 設定を完了

#### 4. 環境変数の設定（Secret Managerを使用）

```bash
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

#### 5. cloudbuild-github.yamlの更新

Secret Managerから環境変数を読み込むように設定：

```yaml
substitutions:
  _WLSACCESSID: '$(gcloud secrets versions access latest --secret=wlsaccessid)'
  _WLSSECRET: '$(gcloud secrets versions access latest --secret=wlssecret)'
  _LICENSEID: '$(gcloud secrets versions access latest --secret=licenseid)'
```

または、Cloud Buildトリガーの設定で環境変数を直接指定することも可能です。

### デプロイの実行

GitHubのmainブランチにプッシュすると、自動的にデプロイが開始されます：

```bash
git add .
git commit -m "Deploy to Cloud Run"
git push origin main
```

### デプロイの確認

```bash
# Cloud Buildの履歴を確認
gcloud builds list --limit=5

# 最新のビルドログを確認
gcloud builds log $(gcloud builds list --limit=1 --format="value(id)")

# Cloud Runサービスの状態を確認
gcloud run services describe $SERVICE_NAME --region $REGION
```

---

## 方法2: ソースベースデプロイ（gcloudコマンド）

ローカルからソースコードを直接デプロイする方法です。

### セットアップ

```bash
# プロジェクトIDを設定
PROJECT_ID="your-project-id"
SERVICE_NAME="timetable-api"
REGION="asia-northeast1"

# 環境変数を設定
export WLSACCESSID="your-wlsaccessid"
export WLSSECRET="your-wlssecret"
export LICENSEID="your-licenseid"
```

### デプロイの実行

```bash
# デプロイスクリプトを使用
./deploy-github.sh $PROJECT_ID $SERVICE_NAME $REGION

# または、直接gcloudコマンドを使用
gcloud run deploy $SERVICE_NAME \
    --source . \
    --region $REGION \
    --platform managed \
    --allow-unauthenticated \
    --port 8080 \
    --memory 2Gi \
    --cpu 2 \
    --timeout 3600 \
    --max-instances 10 \
    --set-env-vars "WLSACCESSID=$WLSACCESSID,WLSSECRET=$WLSSECRET,LICENSEID=$LICENSEID,CBC_PATH=/usr/bin/cbc"
```

### 注意点

- ソースベースデプロイは、Cloud Buildを使用して自動的にビルドします
- ビルド時間は通常5-10分かかります
- ビルドログはCloud Buildで確認できます

---

## 方法3: GitHub Actionsを使用

GitHub ActionsでCloud Runにデプロイする方法です。

### .github/workflows/deploy.yml の作成

```yaml
name: Deploy to Cloud Run

on:
  push:
    branches:
      - main

env:
  PROJECT_ID: your-project-id
  SERVICE_NAME: timetable-api
  REGION: asia-northeast1

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - id: 'auth'
        uses: 'google-github-actions/auth@v1'
        with:
          credentials_json: '${{ secrets.GCP_SA_KEY }}'

      - name: 'Set up Cloud SDK'
        uses: 'google-github-actions/setup-gcloud@v1'

      - name: 'Deploy to Cloud Run'
        run: |
          gcloud run deploy ${{ env.SERVICE_NAME }} \
            --source . \
            --region ${{ env.REGION }} \
            --platform managed \
            --allow-unauthenticated \
            --port 8080 \
            --memory 2Gi \
            --cpu 2 \
            --timeout 3600 \
            --max-instances 10 \
            --set-env-vars "WLSACCESSID=${{ secrets.WLSACCESSID }},WLSSECRET=${{ secrets.WLSSECRET }},LICENSEID=${{ secrets.LICENSEID }},CBC_PATH=/usr/bin/cbc"
```

### GitHub Secretsの設定

1. GitHubリポジトリの Settings → Secrets and variables → Actions
2. 以下のSecretsを追加：
   - `GCP_SA_KEY`: Google CloudサービスアカウントのJSONキー
   - `WLSACCESSID`: GurobiライセンスID
   - `WLSSECRET`: Gurobiライセンスシークレット
   - `LICENSEID`: GurobiライセンスID

### サービスアカウントキーの作成

```bash
# サービスアカウントを作成
gcloud iam service-accounts create github-actions \
    --display-name="GitHub Actions Service Account"

# 権限を付与
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:github-actions@${PROJECT_ID}.iam.gserviceaccount.com" \
    --role="roles/run.admin"

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:github-actions@${PROJECT_ID}.iam.gserviceaccount.com" \
    --role="roles/iam.serviceAccountUser"

# JSONキーを生成
gcloud iam service-accounts keys create key.json \
    --iam-account=github-actions@${PROJECT_ID}.iam.gserviceaccount.com

# key.jsonの内容をGitHub SecretsのGCP_SA_KEYに設定
```

---

## トラブルシューティング

### 1. ビルドエラー

- Dockerfileの構文を確認
- 依存関係が正しくインストールされているか確認
- Cloud Buildのログを確認: `gcloud builds log BUILD_ID`

### 2. 権限エラー

- Cloud Buildサービスアカウントに適切な権限が付与されているか確認
- IAMポリシーを確認: `gcloud projects get-iam-policy $PROJECT_ID`

### 3. 環境変数エラー

- Secret ManagerにSecretが正しく作成されているか確認
- Cloud BuildサービスアカウントにSecretへのアクセス権限があるか確認

### 4. デプロイタイムアウト

- ビルド時間が長い場合は、Cloud Buildのタイムアウト設定を調整
- マシンタイプを変更: `machineType: 'E2_HIGHCPU_8'`

---

## 比較: Artifact Registry vs GitHub直接デプロイ

詳細は `DEPLOY_COMPARISON.md` を参照してください。

### 簡易比較

| 項目 | Artifact Registry | GitHub直接 |
|------|------------------|-----------|
| セットアップ | 中 | 低 |
| デプロイ速度 | 速（3-5分） | 遅（5-10分） |
| コスト | 中 | 低 |
| 自動デプロイ | CI/CD設定必要 | トリガーで自動 |

---

## 参考リンク

- [Cloud Build ドキュメント](https://cloud.google.com/build/docs)
- [Cloud Run ソースベースデプロイ](https://cloud.google.com/run/docs/deploying/source-code)
- [GitHub Actions for Google Cloud](https://github.com/google-github-actions)
