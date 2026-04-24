from sqlalchemy.orm import Session
from database import SavedPost, PostVote, User
from schemas.social_schemas import SavePostRequest

def save_post(db: Session, user_id: int, req: SavePostRequest) -> SavedPost:
    post = SavedPost(
        user_id=user_id,
        title=req.title,
        subreddit=req.subreddit,
        url=req.url,
        upvotes=req.upvotes,
        sentiment=req.sentiment,
        image_url=req.image_url
    )
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

def get_all_posts(db: Session) -> list[SavedPost]:
    return db.query(SavedPost).order_by(SavedPost.created_at.desc()).all()

def get_post_by_id(db: Session, post_id: int) -> SavedPost:
    return db.query(SavedPost).filter(SavedPost.id == post_id).first()

def vote_post(db: Session, user_id: int, post_id: int, vote_type: str) -> dict:
    existing = db.query(PostVote).filter(
        PostVote.user_id == user_id,
        PostVote.post_id == post_id
    ).first()

    post = db.query(SavedPost).filter(SavedPost.id == post_id).first()
    if not post:
        return {"error": "Post not found"}

    if existing:
        if existing.vote_type == vote_type:
            # ── Toggle off same vote ──
            db.delete(existing)
            post.upvotes += -1 if vote_type == "up" else 1
            db.commit()
            return {"vote_type": None, "upvotes": post.upvotes}
        else:
            # ── Switch vote ──
            existing.vote_type = vote_type
            post.upvotes += 2 if vote_type == "up" else -2
            db.commit()
            return {"vote_type": vote_type, "upvotes": post.upvotes}
    else:
        # ── New vote ──
        new_vote = PostVote(user_id=user_id, post_id=post_id, vote_type=vote_type)
        db.add(new_vote)
        post.upvotes += 1 if vote_type == "up" else -1
        db.commit()
        return {"vote_type": vote_type, "upvotes": post.upvotes}

def get_user_vote(db: Session, user_id: int, post_id: int) -> str | None:
    vote = db.query(PostVote).filter(
        PostVote.user_id == user_id,
        PostVote.post_id == post_id
    ).first()
    return vote.vote_type if vote else None