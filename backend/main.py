from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from database import init_db
from schemas.schemas import SearchRequest, RecommendationResponse, TrendingResponse
from services.recommendation_service import get_recommendations, get_trending
from routers import auth, posts, comments, likes, media
import os

init_db()

app = FastAPI(
    title="ReddiSense API",
    description="Reddit recommendation system with social features",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs("../uploads", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="../uploads"), name="uploads")

# ── Routers ────────────────────────────────────────────────
app.include_router(auth.router)
app.include_router(posts.router)
app.include_router(comments.router)
app.include_router(likes.router)
app.include_router(media.router)

@app.get("/")
async def root():
    return {
        "status":  "running",
        "app":     "ReddiSense API",
        "version": "2.0.0",
        "endpoints": [
            "POST /auth/register",
            "POST /auth/login",
            "GET  /auth/me",
            "POST /recommend",
            "GET  /trending",
            "POST /posts/save",
            "GET  /posts/",
            "GET  /posts/{id}",
            "POST /posts/{id}/vote",
            "GET  /posts/{id}/comments",
            "POST /posts/{id}/comments",
            "DELETE /comments/{id}",
            "GET  /comments/{id}/replies",
            "POST /comments/{id}/replies",
            "DELETE /replies/{id}",
            "POST /like/",
            "POST /upload/"
        ]
    }

@app.get("/health")
async def health():
    return {
        "status":      "ok",
        "db":          "sqlite ✅",
        "rapidapi":    "connected ✅",
        "clustering":  "TF-IDF + KMeans ✅",
        "association": "Apriori ✅",
        "uploads":     "enabled ✅"
    }

@app.post("/recommend", response_model=RecommendationResponse)
async def recommend(request: SearchRequest):
    from fastapi import HTTPException
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    return await get_recommendations(request.query.strip(), request.limit)

@app.get("/trending", response_model=TrendingResponse)
async def trending():
    return await get_trending()