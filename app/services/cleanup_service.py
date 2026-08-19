import os

from sqlalchemy.orm import Session

from app.repositories.upload_repository import UploadRepository


def cleanup_expired_uploads(db: Session):

    expired_uploads = UploadRepository.get_expired(db)

    deleted_count = 0

    for upload in expired_uploads:

        if upload.file_path:
            if os.path.exists(upload.file_path):
                os.remove(upload.file_path)

        UploadRepository.delete(db, upload)

        deleted_count += 1

    return deleted_count