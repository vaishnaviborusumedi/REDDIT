import httpx
from datetime import date
from config import HEADERS, RAPIDAPI_HOST
from schemas.schemas import TrendingTopic

BASE_URL = f"https://{RAPIDAPI_HOST}"

def get_momentum(upvotes: int) -> str:
    if upvotes >= 20000:
        return "viral"
    elif upvotes >= 5000:
        return "trending"
    else:
        return "emerging"

async def fetch_trending_topics() -> list[TrendingTopic]:
    async with httpx.AsyncClient() as client:
        try:
            print("[trending_service] Fetching trending topics...")

            response = await client.get(
                f"{BASE_URL}/getPopularPosts",
                headers=HEADERS,
                params={"sort": "hot"},
                timeout=15
            )
            response.raise_for_status()
            data = response.json()

            # ── Parse response ──
            raw_posts = data.get("data", {}).get("posts", [])

            # fallback if posts key differs
            if not raw_posts and isinstance(data.get("data"), list):
                raw_posts = data["data"]

            topics = []
            seen_titles = set()

            for item in raw_posts[:50]:
                p = item.get("data", item)

                title     = p.get("title", "").strip()
                subreddit = p.get("subreddit", "unknown")
                upvotes   = p.get("ups", p.get("score", 0))

                if not title or title in seen_titles:
                    continue

                seen_titles.add(title)

                topics.append(TrendingTopic(
                    topic=title,
                    subreddit=subreddit,
                    upvotes=upvotes,
                    momentum=get_momentum(upvotes)
                ))

            # ── Sort by upvotes descending ──
            topics.sort(key=lambda x: x.upvotes, reverse=True)

            print(f"[trending_service] Found {len(topics)} trending topics")
            return topics[:20]

        except Exception as e:
            print(f"[trending_service] Error: {e}")
            return []