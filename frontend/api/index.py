import sys
import os

# プロジェクトルート（frontendの親ディレクトリ）をパスに追加
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'backend'))

# backend/app/main.py から app をインポート
from app.main import app
