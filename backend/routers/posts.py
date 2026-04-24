from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db, User
from routers.auth import get_current_user
from crud.post_crud import (
    save_post, get_all_posts,
    get_post_by_id, vote_post, get_user_vote
)
from schemas.social_schemas import (
    SavePostRequest, PostOut, VoteRequest
)

router = APIRouter(prefix="/posts", tags=["Posts"])

# ── Save a Reddit post ─────────────────────────────────────
@router.post("/save", response_model=PostOut)
def save(
    req: SavePostRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    post = save_post(db, current_user.id, req)
    post_out = PostOut(
        id=post.id,
        title=post.title,
        subreddit=post.subreddit,
        url=post.url,
        upvotes=post.upvotes,
        sentiment=post.sentiment,
        image_url=post.image_url,
        created_at=post.created_at,
        comment_count=0,
        user_vote=None
    )
    print(f"[posts] Post saved by {current_user.username}: {post.title[:40]}")
    return post_out

# ── Get all posts ──────────────────────────────────────────
@router.get("/", response_model=list[PostOut])
def get_posts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    posts = get_all_posts(db)
    result = []
    for post in posts:
        result.append(PostOut(
            id=post.id,
            title=post.title,
            subreddit=post.subreddit,
            url=post.url,
            upvotes=post.upvotes,
            sentiment=post.sentiment,
            image_url=post.image_url,
            created_at=post.created_at,
            comment_count=len(post.comments),
            user_vote=get_user_vote(db, current_user.id, post.id)
        ))
    return result

# ── Get single post ────────────────────────────────────────
@router.get("/{post_id}", response_model=PostOut)
def get_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    post = get_post_by_id(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    return PostOut(
        id=post.id,
        title=post.title,
        subreddit=post.subreddit,
        url=post.url,
        upvotes=post.upvotes,
        sentiment=post.sentiment,
        image_url=post.image_url,
        created_at=post.created_at,
        comment_count=len(post.comments),
        user_vote=get_user_vote(db, current_user.id, post.id)
    )

# ── Vote on a post ─────────────────────────────────────────
@router.post("/{post_id}/vote")
def vote(
    post_id: int,
    req: VoteRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if req.vote_type not in ["up", "down"]:
        raise HTTPException(status_code=400, detail="vote_type must be 'up' or 'down'")

    result = vote_post(db, current_user.id, post_id, req.vote_type)
    print(f"[posts] {current_user.username} voted '{req.vote_type}' on post {post_id}")
    return result