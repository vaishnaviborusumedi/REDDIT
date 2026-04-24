from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional, List
from datetime import datetime

class RegisterRequest(BaseModel):
    username: str
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    username: str
    user_id: int

class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    username: str
    email: str
    avatar_url: Optional[str] = None
    created_at: datetime

class SavePostRequest(BaseModel):
    title: str
    subreddit: str
    url: str
    upvotes: int
    sentiment: str
    image_url: Optional[str] = None

class PostOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    subreddit: str
    url: str
    upvotes: int
    sentiment: str
    image_url: Optional[str] = None
    created_at: datetime
    comment_count: Optional[int] = 0
    user_vote: Optional[str] = None

class VoteRequest(BaseModel):
    vote_type: str

class CommentCreate(BaseModel):
    content: str
    image_url: Optional[str] = None

class ReplyOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: int
    username: str
    content: str
    image_url: Optional[str] = None
    like_count: int = 0
    user_liked: bool = False
    created_at: datetime

class CommentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: int
    username: str
    content: str
    image_url: Optional[str] = None
    upvotes: int = 0
    like_count: int = 0
    user_liked: bool = False
    created_at: datetime
    replies: List[ReplyOut] = []

class ReplyCreate(BaseModel):
    content: str
    image_url: Optional[str] = None

class LikeRequest(BaseModel):
    target_id: int
    target_type: str

class LikeResponse(BaseModel):
    liked: bool
    like_count: int

class UploadResponse(BaseModel):
    image_url: str
    filename: str