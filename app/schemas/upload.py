from pydantic import BaseModel
from typing import Optional


class TextUpload(BaseModel):
    text: str


class UploadResponse(BaseModel):
    code: str
    message: str


class ShareResponse(BaseModel):
    code: str
    type: str

    text_content: Optional[str] = None
    file_name: Optional[str] = None