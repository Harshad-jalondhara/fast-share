from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import TextUpload, UploadResponse
from app.services.upload_service import create_text_upload

router = APIRouter(
    prefix="/upload",
    tags=["Upload"]
)


@router.post("/text", response_model=UploadResponse)
def upload_text(data: TextUpload, db: Session = Depends(get_db)):

    upload = create_text_upload(data.text, db)

    return {
        "code": upload.code,
        "message": "Text uploaded successfully"
    }