from sqlalchemy.orm import Session
from database import Comment, Reply, Like, User

def create_comment(db: Session, user_id: int, post_id: int, content: str, image_url: str = None) -> Comment:
    comment = Comment(
        user_id=user_id,
        post_id=post_id,
        content=content,
        image_url=image_url
    )
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment

def get_comments_by_post(db: Session, post_id: int) -> list[Comment]:
    return db.query(Comment).filter(
        Comment.post_id == post_id
    ).order_by(Comment.created_at.desc()).all()

def get_comment_by_id(db: Session, comment_id: int) -> Comment:
    return db.query(Comment).filter(Comment.id == comment_id).first()

def delete_comment(db: Session, comment_id: int, user_id: int) -> bool:
    comment = db.query(Comment).filter(
        Comment.id == comment_id,
        Comment.user_id == user_id
    ).first()
    if not comment:
        return False
    db.delete(comment)
    db.commit()
    return True

def create_reply(db: Session, user_id: int, comment_id: int, content: str, image_url: str = None) -> Reply:
    reply = Reply(
        user_id=user_id,
        comment_id=comment_id,
        content=content,
        image_url=image_url
    )
    db.add(reply)
    db.commit()
    db.refresh(reply)
    return reply

def get_replies_by_comment(db: Session, comment_id: int) -> list[Reply]:
    return db.query(Reply).filter(
        Reply.comment_id == comment_id
    ).order_by(Reply.created_at.asc()).all()

def delete_reply(db: Session, reply_id: int, user_id: int) -> bool:
    reply = db.query(Reply).filter(
        Reply.id == reply_id,
        Reply.user_id == user_id
    ).first()
    if not reply:
        return False
    db.delete(reply)
    db.commit()
    return True

def get_like_count(db: Session, comment_id: int = None, reply_id: int = None) -> int:
    query = db.query(Like)
    if comment_id:
        query = query.filter(Like.comment_id == comment_id)
    if reply_id:
        query = query.filter(Like.reply_id == reply_id)
    return query.count()

def user_liked(db: Session, user_id: int, comment_id: int = None, reply_id: int = None) -> bool:
    query = db.query(Like).filter(Like.user_id == user_id)
    if comment_id:
        query = query.filter(Like.comment_id == comment_id)
    if reply_id:
        query = query.filter(Like.reply_id == reply_id)
    return query.first() is not None