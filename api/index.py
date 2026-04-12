import os
import sys

# プロジェクトのルートディレクトリをパスに追加
# これにより 'backend' モジュールが見つかるようにする
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

try:
    # 'backend.app.main' としてインポートを試みる
    from backend.app.main import app
except ImportError as e:
    # 失敗した場合のフォールバック
    print(f"Import Error: {e}")
    # 最小限のアプリを返して 404/500 の原因を切り分ける
    from fastapi import FastAPI
    app = FastAPI()
    @app.get("/api/v1/debug")
    async def debug():
        return {"error": str(e), "sys_path": sys.path}

# Vercel は 'app' という名前の FastAPI インスタンスを探す
