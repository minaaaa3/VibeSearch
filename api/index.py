import os
import sys

# 開発環境でもデプロイ環境でも 'backend' を見つけられるようにパスを調整
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

# FastAPI インスタンスのインポート
try:
    from backend.app.main import app
except ImportError as e:
    # 起動時のインポートエラーをデバッグしやすくするため、エラーを FastAPI に吐かせる
    from fastapi import FastAPI
    app = FastAPI()
    @app.get("/api/debug")
    async def debug():
        return {"error": str(e), "path": sys.path}

# Vercel は 'app' という変数名を探します
