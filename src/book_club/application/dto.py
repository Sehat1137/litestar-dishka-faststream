from dataclasses import dataclass


@dataclass(slots=True)
class NewBookDTO:
    title: str
    pages: int
    is_read: bool
