from sqlalchemy.orm import Session
from database import Like

def toggle_like(db: Session, user_id: int, target_id: int, target_type: str) -> dict:
    """
    Toggle like on a comment or reply.
    Returns liked status and new like count.
    """
    if target_type == "comment":
        existing = db.query(Like).filter(
            Like.user_id == user_id,
            Like.comment_id == target_id
        ).first()

        if existing:
            db.delete(existing)
            db.commit()
            count = db.query(Like).filter(Like.comment_id == target_id).count()
            return {"liked": False, "like_count": count}
        else:
            like = Like(user_id=user_id, comment_id=target_id)
            db.add(like)
            db.commit()
            count = db.query(Like).filter(Like.comment_id == target_id).count()
            return {"liked": True, "like_count": count}

    elif target_type == "reply":
        existing = db.query(Like).filter(
            Like.user_id == user_id,
            Like.reply_id == target_id
        ).first()

        if existing:
            db.delete(existing)
            db.commit()
            count = db.query(Like).filter(Like.reply_id == target_id).count()
            return {"liked": False, "like_count": count}
        else:
            like = Like(user_id=user_id, reply_id=target_id)
            db.add(like)
            db.commit()
            count = db.query(Like).filter(Like.reply_id == target_id).count()
            return {"liked": True, "like_count": count}

    return {"error": "Invalid target_type"}