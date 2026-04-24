import os
import uuid
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from PIL import Image
import aiofiles
from database import User
from routers.auth import get_current_user
from schemas.social_schemas import UploadResponse

router = APIRouter(prefix="/upload", tags=["Media"])

# ── Config ─────────────────────────────────────────────────
UPLOAD_DIR     = "../uploads"
MAX_SIZE_MB    = 5
ALLOWED_TYPES  = {"image/jpeg", "image/png", "image/gif", "image/webp"}

os.makedirs(UPLOAD_DIR, exist_ok=True)

# ── Upload Image ───────────────────────────────────────────
@router.post("/", response_model=UploadResponse)
async def upload_image(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    # ── Validate file type ──
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"File type not allowed. Use: jpeg, png, gif, webp"
        )

    # ── Read file ──
    contents = await file.read()

    # ── Validate file size ──
    size_mb = len(contents) / (1024 * 1024)
    if size_mb > MAX_SIZE_MB:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Max size is {MAX_SIZE_MB}MB"
        )

    # ── Generate unique filename ──
    ext      = file.filename.split(".")[-1].lower()
    filename = f"{uuid.uuid4().hex}.{ext}"
    filepath = os.path.join(UPLOAD_DIR, filename)

    # ── Save file ──
    async with aiofiles.open(filepath, "wb") as f:
        await f.write(contents)

    # ── Optimize image with Pillow ──
    try:
        img = Image.open(filepath)

        # Resize if too large (max 1200px width)
        if img.width > 1200:
            ratio  = 1200 / img.width
            height = int(img.height * ratio)
            img    = img.resize((1200, height), Image.LANCZOS)

        # Convert RGBA to RGB for jpeg
        if img.mode == "RGBA" and ext in ["jpg", "jpeg"]:
            img = img.convert("RGB")

        img.save(filepath, optimize=True, quality=85)
        print(f"[media] Image optimized and saved: {filename}")

    except Exception as e:
        print(f"[media] Pillow optimization warning: {e}")

    image_url = f"http://localhost:8000/uploads/{filename}"
    print(f"[media] {current_user.username} uploaded: {filename}")

    return UploadResponse(image_url=image_url, filename=filename)