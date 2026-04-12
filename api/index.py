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

# インポートエラー時に 500 になるのを防ぐために、FastAPI 自身にデバッグ用のエンドポイントを持たせる
from backend.app.main import app

# Vercel は 'app' 変数を探します
