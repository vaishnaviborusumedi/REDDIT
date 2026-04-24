import asyncio
from services.recommendation_service import get_recommendations, get_trending

async def test():
    # ── Test Recommendations ──
    print("=" * 60)
    print("RECOMMENDATION PIPELINE TEST")
    print("=" * 60)

    result = await get_recommendations("artificial intelligence")

    print(f"\n📌 Query: {result.query}")
    print(f"\n🏆 Top 10 Posts:")
    for i, p in enumerate(result.top_10, 1):
        print(f"  {i}. [{p.sentiment.upper()}] {p.title[:60]}")
        print(f"     r/{p.subreddit} | 👍 {p.upvotes}")

    print(f"\n🔗 Association Rules ({len(result.associations)}):")
    for r in result.associations[:5]:
        print(f"  [{r.antecedent}] → [{r.consequent}] (conf: {r.confidence})")

    print(f"\n🔹 Clusters ({len(result.clusters)}):")
    for c in result.clusters:
        print(f"  Cluster {c.cluster_id}: {c.label} ({len(c.topics)} posts)")

    # ── Test Trending ──
    print("\n" + "=" * 60)
    print("TRENDING TOPICS TEST")
    print("=" * 60)

    trending = await get_trending()
    print(f"\n📅 Date: {trending.date}")
    print(f"🔥 Trending ({len(trending.trending)}):")
    for i, t in enumerate(trending.trending[:5], 1):
        print(f"  {i}. [{t.momentum.upper()}] {t.topic[:60]}")
        print(f"     r/{t.subreddit} | 👍 {t.upvotes}")

asyncio.run(test())