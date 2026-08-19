from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import os

from app.database import get_db
from app.enums import UploadType
from app.models import Upload
from app.schemas import ShareResponse
from app.repositories.upload_repository import UploadRepository
from datetime import datetime

router = APIRouter(prefix="/share", tags=["Share"])

@router.get("/{code}", response_model=ShareResponse)
def get_share(code: str, db: Session = Depends(get_db)):

    upload = UploadRepository.get_by_code(db, code)

    if upload.expires_at <= datetime.utcnow():

        if upload.file_path and os.path.exists(upload.file_path):
            os.remove(upload.file_path)

        UploadRepository.delete(db, upload)

        raise HTTPException(
            status_code=404,
            detail="This share code has expired"
        )

    if not upload:
        raise HTTPException(
            status_code=404,
            detail="Invalid code"
        )

    # text
    if upload.type == UploadType.TEXT:
        return {
            "code": code,
            "type": UploadType.TEXT,
            "text_content": upload.text_content
        }

    # file
    if upload.type == UploadType.FILE:

        if not os.path.exists(upload.file_path):
            raise HTTPException(status_code=404, detail="File not found")


        return FileResponse(
            path=upload.file_path,
            filename=upload.file_name,
            media_type="application/octet-stream"
        )

    raise HTTPException(
        status_code=400,
        detail="Invalid upload type"
    )