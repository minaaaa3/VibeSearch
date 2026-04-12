import os
import sys

# プロジェクトルートをパスに追加
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

# backend フォルダもパスに追加
backend_dir = os.path.join(root_dir, 'backend')
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from fastapi import FastAPI
try:
    # 既存のバックエンド設定を読み込む
    from backend.app.main import app as main_app
    
    # Vercel 用のラッパー
    app = FastAPI()
    
    # すべてのリクエストを既存の main_app に委譲する（マウント）
    # これにより /api/xxx が main_app のルートとして機能する
    app.mount("/api", main_app)
    
except ImportError as e:
    app = FastAPI()
    @app.get("/api/debug")
    async def debug():
        return {"error": str(e), "sys_path": sys.path}

# Vercel は 'app' という変数名を探します
