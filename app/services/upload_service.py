from sqlalchemy.orm import Session

from app.models import Upload
from app.utils import generate_code


def create_text_upload(text: str, db: Session):

    code = generate_code(db)

    upload = Upload(
        code=code,
        type="text",
        text_content=text
    )

    db.add(upload)
    db.commit()
    db.refresh(upload)

    return upload