import os
import shutil
from fastapi import UploadFile

from sqlalchemy.orm import Session

from app.enums import UploadType
from app.models import Upload
from app.utils import generate_code

from app.repositories.upload_repository import UploadRepository


UPLOAD_FOLDER = "uploads"


def create_file_upload(file: UploadFile, db: Session):
    code = generate_code(db)

    file_path = os.path.join(UPLOAD_FOLDER, f"{code}_{file.filename}")

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    upload = Upload(
        code = code,
        type=UploadType.FILE,
        file_name = file.filename,
        file_path = file_path
    )

    return UploadRepository.create(db, upload)

def create_text_upload(text: str, db: Session):

    code = generate_code(db)

    upload = Upload(
        code=code,
        type=UploadType.TEXT,
        text_content=text
    )

    return UploadRepository.create(db, upload)