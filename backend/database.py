from sqlalchemy import (
    create_engine, Column, Integer, String,
    Text, DateTime, ForeignKey, Enum
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import enum

# ── SQLite Database ────────────────────────────────────────
DATABASE_URL = "sqlite:///./reddisense.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ── Dependency for FastAPI routes ──────────────────────────
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ══════════════════════════════════════════════════════════
# MODELS
# ══════════════════════════════════════════════════════════

class User(Base):
    __tablename__ = "users"

    id            = Column(Integer, primary_key=True, index=True)
    username      = Column(String(50), unique=True, index=True, nullable=False)
    email         = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    avatar_url    = Column(String(500), nullable=True)
    created_at    = Column(DateTime, default=datetime.utcnow)

    # relationships
    saved_posts   = relationship("SavedPost", back_populates="user")
    comments      = relationship("Comment", back_populates="user")
    replies       = relationship("Reply", back_populates="user")
    likes         = relationship("Like", back_populates="user")
    votes         = relationship("PostVote", back_populates="user")


class SavedPost(Base):
    __tablename__ = "saved_posts"

    id          = Column(Integer, primary_key=True, index=True)
    user_id     = Column(Integer, ForeignKey("users.id"), nullable=False)
    title       = Column(Text, nullable=False)
    subreddit   = Column(String(100))
    url         = Column(String(500))
    upvotes     = Column(Integer, default=0)
    sentiment   = Column(String(20), default="discussed")
    image_url   = Column(String(500), nullable=True)
    created_at  = Column(DateTime, default=datetime.utcnow)

    # relationships
    user        = relationship("User", back_populates="saved_posts")
    comments    = relationship("Comment", back_populates="post", cascade="all, delete")
    votes       = relationship("PostVote", back_populates="post", cascade="all, delete")


class Comment(Base):
    __tablename__ = "comments"

    id          = Column(Integer, primary_key=True, index=True)
    user_id     = Column(Integer, ForeignKey("users.id"), nullable=False)
    post_id     = Column(Integer, ForeignKey("saved_posts.id"), nullable=False)
    content     = Column(Text, nullable=False)
    image_url   = Column(String(500), nullable=True)
    upvotes     = Column(Integer, default=0)
    created_at  = Column(DateTime, default=datetime.utcnow)

    # relationships
    user        = relationship("User", back_populates="comments")
    post        = relationship("SavedPost", back_populates="comments")
    replies     = relationship("Reply", back_populates="comment", cascade="all, delete")
    likes       = relationship("Like", back_populates="comment", cascade="all, delete")


class Reply(Base):
    __tablename__ = "replies"

    id          = Column(Integer, primary_key=True, index=True)
    user_id     = Column(Integer, ForeignKey("users.id"), nullable=False)
    comment_id  = Column(Integer, ForeignKey("comments.id"), nullable=False)
    content     = Column(Text, nullable=False)
    image_url   = Column(String(500), nullable=True)
    created_at  = Column(DateTime, default=datetime.utcnow)

    # relationships
    user        = relationship("User", back_populates="replies")
    comment     = relationship("Comment", back_populates="replies")
    likes       = relationship("Like", back_populates="reply", cascade="all, delete")


class Like(Base):
    __tablename__ = "likes"

    id          = Column(Integer, primary_key=True, index=True)
    user_id     = Column(Integer, ForeignKey("users.id"), nullable=False)
    comment_id  = Column(Integer, ForeignKey("comments.id"), nullable=True)
    reply_id    = Column(Integer, ForeignKey("replies.id"), nullable=True)
    created_at  = Column(DateTime, default=datetime.utcnow)

    # relationships
    user        = relationship("User", back_populates="likes")
    comment     = relationship("Comment", back_populates="likes")
    reply       = relationship("Reply", back_populates="likes")


class PostVote(Base):
    __tablename__ = "post_votes"

    id          = Column(Integer, primary_key=True, index=True)
    user_id     = Column(Integer, ForeignKey("users.id"), nullable=False)
    post_id     = Column(Integer, ForeignKey("saved_posts.id"), nullable=False)
    vote_type   = Column(String(10), nullable=False)   # "up" or "down"
    created_at  = Column(DateTime, default=datetime.utcnow)

    # relationships
    user        = relationship("User", back_populates="votes")
    post        = relationship("SavedPost", back_populates="votes")


# ── Create all tables ──────────────────────────────────────
def init_db():
    Base.metadata.create_all(bind=engine)
    print("[database] All tables created ✅")