from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db, User
from routers.auth import get_current_user
from crud.comment_crud import (
    create_comment, get_comments_by_post,
    get_comment_by_id, delete_comment,
    create_reply, get_replies_by_comment,
    delete_reply, get_like_count, user_liked
)
from crud.post_crud import get_post_by_id
from schemas.social_schemas import (
    CommentCreate, CommentOut,
    ReplyCreate, ReplyOut
)

router = APIRouter(tags=["Comments & Replies"])

# ── Helper to build ReplyOut ───────────────────────────────
def build_reply_out(reply, db: Session, user_id: int) -> ReplyOut:
    return ReplyOut(
        id=reply.id,
        user_id=reply.user_id,
        username=reply.user.username,
        content=reply.content,
        image_url=reply.image_url,
        like_count=get_like_count(db, reply_id=reply.id),
        user_liked=user_liked(db, user_id, reply_id=reply.id),
        created_at=reply.created_at
    )

# ── Helper to build CommentOut ─────────────────────────────
def build_comment_out(comment, db: Session, user_id: int) -> CommentOut:
    replies = get_replies_by_comment(db, comment.id)
    return CommentOut(
        id=comment.id,
        user_id=comment.user_id,
        username=comment.user.username,
        content=comment.content,
        image_url=comment.image_url,
        upvotes=comment.upvotes,
        like_count=get_like_count(db, comment_id=comment.id),
        user_liked=user_liked(db, user_id, comment_id=comment.id),
        created_at=comment.created_at,
        replies=[build_reply_out(r, db, user_id) for r in replies]
    )

# ══════════════════════════════════════════════════════════
# COMMENT ROUTES
# ══════════════════════════════════════════════════════════

# ── Get all comments on a post ─────────────────────────────
@router.get("/posts/{post_id}/comments", response_model=list[CommentOut])
def get_comments(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    post = get_post_by_id(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    comments = get_comments_by_post(db, post_id)
    return [build_comment_out(c, db, current_user.id) for c in comments]

# ── Add comment to a post ──────────────────────────────────
@router.post("/posts/{post_id}/comments", response_model=CommentOut)
def add_comment(
    post_id: int,
    req: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    post = get_post_by_id(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    comment = create_comment(
        db, current_user.id, post_id,
        req.content, req.image_url
    )
    print(f"[comments] {current_user.username} commented on post {post_id}")
    return build_comment_out(comment, db, current_user.id)

# ── Delete a comment ───────────────────────────────────────
@router.delete("/comments/{comment_id}")
def remove_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    success = delete_comment(db, comment_id, current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Comment not found or not yours")
    return {"message": "Comment deleted"}

# ══════════════════════════════════════════════════════════
# REPLY ROUTES
# ══════════════════════════════════════════════════════════

# ── Get replies to a comment ───────────────────────────────
@router.get("/comments/{comment_id}/replies", response_model=list[ReplyOut])
def get_replies(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    comment = get_comment_by_id(db, comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    replies = get_replies_by_comment(db, comment_id)
    return [build_reply_out(r, db, current_user.id) for r in replies]

# ── Reply to a comment ─────────────────────────────────────
@router.post("/comments/{comment_id}/replies", response_model=ReplyOut)
def add_reply(
    comment_id: int,
    req: ReplyCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    comment = get_comment_by_id(db, comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    reply = create_reply(
        db, current_user.id, comment_id,
        req.content, req.image_url
    )
    print(f"[comments] {current_user.username} replied to comment {comment_id}")
    return build_reply_out(reply, db, current_user.id)

# ── Delete a reply ─────────────────────────────────────────
@router.delete("/replies/{reply_id}")
def remove_reply(
    reply_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    success = delete_reply(db, reply_id, current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Reply not found or not yours")
    return {"message": "Reply deleted"}