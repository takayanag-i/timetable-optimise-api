# Optimisation API

時間割編成を最適化するためのREST APIです。

## ローカル開発

### サーバーの起動

```shell
PYTHONPATH=./src uv run uvicorn main:app --reload --host 0.0.0.0 --port 8001
```

docker-composeがあるディレクトリから実行する場合
```shell
docker-compose exec fastapi sh -c "cd /workspaces/timetable/fastapi && PYTHONPATH=./src uv run uvicorn main:app --reload --host 0.0.0.0 --port 8001"
```

### OpenAPI ドキュメント

[http://localhost:8001/docs](http://localhost:8001/docs)

## Cloud Runへのデプロイ

GitHubからCloud Buildトリガーを使用してCloud Runにデプロイします。詳細は [DEPLOY.md](./DEPLOY.md) を参照してください。

### クイックスタート

1. **Cloud Buildトリガーの設定**
   - [Cloud Console](https://console.cloud.google.com/cloud-build/triggers) からGitHubリポジトリを接続
   - `cloudbuild-github.yaml` をビルド設定として指定
   - 環境変数を設定（Secret Managerまたは直接指定）

2. **デプロイの実行**
   - mainブランチにプッシュすると自動的にデプロイが開始されます
   ```bash
   git push origin main
   ```