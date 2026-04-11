import sys
import os

# プロジェクトルートをパスに追加してインポートを可能にする
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

# backend/app/main.py から app をインポート
from app.main import app
