import sys
import os

# プロジェクトルートをパスに追加して backend フォルダを読み込めるようにする
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

# backend/app/main.py から FastAPI の app インスタンスをインポート
from app.main import app
