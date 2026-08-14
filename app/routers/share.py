from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Upload
from app.schemas import ShareResponse

router = APIRouter(prefix="/share", tags=["Share"])

@router.get("/{code}", response_model=ShareResponse)
def get_share(code: str, db: Session = Depends(get_db)):

    upload = db.query(Upload).filter(Upload.code == code).first()

    if not upload:
        raise HTTPException(
            status_code=404,
            detail="code not found"
        )

    return {
        "code": upload.code,
        "type": upload.type,
        "text_content": upload.text_content,
        "file_name": upload.file_name
    }


