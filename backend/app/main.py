from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.search import router as search_router

app = FastAPI(title="VibeSearch API")

# CORSの設定を緩和
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # デバッグのため一時的にすべて許可
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# APIルーターの登録
app.include_router(search_router, prefix="/api/v1", tags=["search"])

@app.get("/")
async def root():
    return {"message": "Welcome to VibeSearch API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
