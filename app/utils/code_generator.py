import random

from sqlalchemy.orm import Session

from app.models import Upload


def generate_code(db: Session):
    while True:
        code = str(random.randint(1000, 9999))

        existing = db.query(Upload).filter(Upload.code == code).first()

        if not existing:
            return code
