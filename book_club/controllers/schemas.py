from pydantic import BaseModel


class BookSchema(BaseModel):
    title: str
    pages: int
    is_read: bool
