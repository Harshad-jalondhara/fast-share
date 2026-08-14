import random

from sqlalchemy.orm import Session

from app.repositories.upload_repository import UploadRepository

def generate_code(db: Session):
    while True:
        code = str(random.randint(1000, 9999))

        upload = UploadRepository.get_by_code(db, code)

        if upload is None:
            return code
