from schemas.schemas import RedditPost, RecommendationResponse, TrendingResponse
from services.reddit_service import fetch_posts_by_query
from services.trending_service import fetch_trending_topics
from models.clustering import cluster_titles
from models.association_rules import build_association_rules
from datetime import date

async def get_recommendations(query: str, limit: int = 10) -> RecommendationResponse:
    """
    Full pipeline:
    1. Fetch posts for query
    2. Cluster them
    3. Build association rules
    4. Return top 10 + clusters + rules
    """
    print(f"\n[recommendation] Starting pipeline for: '{query}'")

    # ── Step 1: Fetch posts ──
    posts = await fetch_posts_by_query(query)

    if not posts:
        print("[recommendation] No posts found")
        return RecommendationResponse(
            query=query,
            top_10=[],
            associations=[],
            clusters=[]
        )

    # ── Step 2: Sort by upvotes → top 10 ──
    sorted_posts = sorted(posts, key=lambda x: x.upvotes, reverse=True)
    top_10 = sorted_posts[:limit]

    # ── Step 3: Extract titles for ML ──
    all_titles = [p.title for p in posts]

    # ── Step 4: Clustering ──
    clusters = cluster_titles(all_titles, n_clusters=min(5, len(all_titles)))

    # ── Step 5: Association rules ──
    associations = build_association_rules(all_titles)

    print(f"[recommendation] Pipeline complete ✅")
    print(f"  Posts: {len(posts)} | Top10: {len(top_10)} | Clusters: {len(clusters)} | Rules: {len(associations)}")

    return RecommendationResponse(
        query=query,
        top_10=top_10,
        associations=associations,
        clusters=clusters
    )


async def get_trending() -> TrendingResponse:
    """Fetch today's trending topics"""
    print("\n[recommendation] Fetching trending topics...")
    topics = await fetch_trending_topics()

    return TrendingResponse(
        date=str(date.today()),
        trending=topics
    )