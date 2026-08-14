from sqlalchemy.orm import Session

from app.models import Upload


class UploadRepository:

    @staticmethod
    def get_by_code(db: Session, code: str):
        return db.query(Upload).filter(Upload.code == code).first()


    @staticmethod
    def create(db: Session, upload: Upload):
        db.add(upload)
        db.commit()
        db.refresh(upload)
        return upload