from dataclasses import dataclass


@dataclass(slots=True)
class BookDM:
    uuid: str
    title: str
    pages: int
    is_read: bool
