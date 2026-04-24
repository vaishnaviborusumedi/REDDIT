import httpx
from config import HEADERS, RAPIDAPI_HOST, MAX_POSTS
from schemas.schemas import RedditPost

BASE_URL = f"https://{RAPIDAPI_HOST}"

def get_sentiment(upvotes: int) -> str:
    if upvotes >= 10000:
        return "hot"
    elif upvotes >= 1000:
        return "rising"
    else:
        return "discussed"

async def fetch_posts_by_query(query: str) -> list[RedditPost]:
    async with httpx.AsyncClient() as client:
        try:
            print(f"[reddit_service] Searching posts for: {query}")
            response = await client.get(
                f"{BASE_URL}/getSearchPosts",
                headers=HEADERS,
                params={"query": query},
                timeout=15
            )
            response.raise_for_status()
            data = response.json()

            # ── Parse response structure ──
            # {"success": true, "data": {"cursor": "...", "posts": [{"data": {...}}, ...]}}
            raw_posts = data.get("data", {}).get("posts", [])

            posts = []
            for item in raw_posts[:MAX_POSTS]:
                # each post is wrapped in {"data": {...}}
                p = item.get("data", item)

                title = p.get("title", "").strip()
                if not title:
                    continue

                upvotes  = p.get("ups", p.get("score", 0))
                post_url = p.get("url", "")
                subreddit = p.get("subreddit", "unknown")

                posts.append(RedditPost(
                    title=title,
                    subreddit=subreddit,
                    upvotes=upvotes,
                    url=post_url,
                    sentiment=get_sentiment(upvotes)
                ))

            print(f"[reddit_service] Fetched {len(posts)} posts")
            return posts

        except Exception as e:
            print(f"[reddit_service] Error: {e}")
            return []

async def fetch_raw_titles(query: str) -> list[str]:
    posts = await fetch_posts_by_query(query)
    return [post.title for post in posts]