from pydantic import BaseModel
from typing import List, Optional

# ─── Request Models ───────────────────────────────────────

class SearchRequest(BaseModel):
    query: str
    limit: int = 10

# ─── Individual Data Models ───────────────────────────────

class RedditPost(BaseModel):
    title: str
    subreddit: str
    upvotes: int
    url: str
    sentiment: Optional[str] = "neutral"  # hot / rising / discussed

class TrendingTopic(BaseModel):
    topic: str
    subreddit: str
    upvotes: int
    momentum: str   # viral / trending / emerging

class AssociationRule(BaseModel):
    antecedent: str       # e.g. "AI"
    consequent: str       # e.g. "Machine Learning"
    confidence: float
    support: float

class ClusterGroup(BaseModel):
    cluster_id: int
    label: str            # e.g. "Technology", "Science"
    topics: List[str]

# ─── Response Models ──────────────────────────────────────

class RecommendationResponse(BaseModel):
    query: str
    top_10: List[RedditPost]
    associations: List[AssociationRule]
    clusters: List[ClusterGroup]

class TrendingResponse(BaseModel):
    date: str
    trending: List[TrendingTopic]