from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db, User
from routers.auth import get_current_user
from crud.like_crud import toggle_like
from schemas.social_schemas import LikeRequest, LikeResponse

router = APIRouter(prefix="/like", tags=["Likes"])

@router.post("/", response_model=LikeResponse)
def like(
    req: LikeRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if req.target_type not in ["comment", "reply"]:
        raise HTTPException(
            status_code=400,
            detail="target_type must be 'comment' or 'reply'"
        )

    result = toggle_like(db, current_user.id, req.target_id, req.target_type)

    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])

    print(f"[likes] {current_user.username} {'liked' if result['liked'] else 'unliked'} {req.target_type} {req.target_id}")
    return LikeResponse(liked=result["liked"], like_count=result["like_count"])