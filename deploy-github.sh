#!/bin/bash

# GitHubから直接Cloud Runにデプロイするスクリプト
# 使用方法: ./deploy-github.sh [PROJECT_ID] [SERVICE_NAME] [REGION]

set -e

# デフォルト値
PROJECT_ID=${1:-"your-project-id"}
SERVICE_NAME=${2:-"timetable-api"}
REGION=${3:-"asia-northeast1"}

# 環境変数の確認
if [ -z "$WLSACCESSID" ] || [ -z "$WLSSECRET" ] || [ -z "$LICENSEID" ]; then
    echo "警告: Gurobiライセンス環境変数が設定されていません"
    echo "WLSACCESSID, WLSSECRET, LICENSEID を設定してください"
    read -p "続行しますか? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo "プロジェクトID: $PROJECT_ID"
echo "サービス名: $SERVICE_NAME"
echo "リージョン: $REGION"

# gcloud認証の確認
echo "gcloud認証を確認しています..."
gcloud config set project $PROJECT_ID

# Container Registry APIの有効化（初回のみ）
echo "Container Registry APIを確認しています..."
gcloud services enable containerregistry.googleapis.com 2>/dev/null || true

# ソースから直接デプロイ（Cloud Runが自動的にビルド）
echo "ソースからCloud Runにデプロイしています..."
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

echo "デプロイが完了しました！"
echo "サービスURLを取得中..."
SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --region $REGION --format="value(status.url)")
echo "サービスURL: $SERVICE_URL"
