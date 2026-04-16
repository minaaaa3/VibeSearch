# VibeSearch

ユーザーの抽象的な「こだわり（感性）」を言語化し、最適なスポットを提案する AI エージェント型検索エンジン。

## プロジェクト概要

VibeSearch は、従来のキーワード検索では表現しきれない「なんとなくこんな雰囲気の場所に行きたい」というユーザーの感性を、AI（Gemini 1.5 Flash）が対話を通じて言語化し、最適なスポットを提案するシステムです。

## 主な機能

- **AI 対話による意図解析**: LangGraph を用いたエージェントが、ユーザーの曖昧な要望を深掘りし、真のニーズを解析します。
- **感性検索 (Vibe Search)**: 「静かで集中できる」「モダンでインスピレーションが湧く」といった抽象的なニュアンスをベクトル検索でマッチング。
- **モダンな UI/UX**: Next.js 15 (App Router) を活用した、レスポンシブで直感的なチャットインターフェース。

## 技術スタック

### Frontend

- **Framework**: Next.js (App Router)
- **Styling**: Tailwind CSS
- **Icons**: Lucide React

### Backend

- **Framework**: FastAPI
- **Agent Framework**: LangGraph
- **LLM**: Gemini 1.5 Flash (langchain-google-genai)

### Infrastructure & Database

- **Database**: Supabase (pgvector, PostGIS)
- **Deployment**: Vercel

## セットアップ

### 環境変数の設定

`.env.local`（フロントエンド）および `backend/.env`（バックエンド）を作成し、必要な API キーを設定してください。

### フロントエンドの起動

```bash
npm install
npm run dev
```

### バックエンドの起動

```bash
cd backend
pip install -r requirements.txt
python -m app.main
```

## デプロイについて

このプロジェクトは **Vercel** にデプロイされています。
フロントエンドと API（Next.js Rewrites または Vercel Functions 経由）がシームレスに連携し、スケーラブルな環境で動作します。
