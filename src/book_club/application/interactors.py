from book_club.application import interfaces
from book_club.application.dto import NewBookDTO
from book_club.domain import entities


class GetBookInteractor:
    def __init__(
            self,
            book_repo: interfaces.BookReader,
    ) -> None:
        self._book_repo = book_repo

    async def __call__(self, uuid: str) -> entities.BookDM | None:
        return await self._book_repo.read_by_uuid(uuid)


class NewBookInteractor:
    def __init__(
            self,
            uow: interfaces.UoW,
            book_repo: interfaces.BookSaver,
            uuid_generator: interfaces.UUIDGenerator,
    ) -> None:
        self._uow = uow
        self._book_repo = book_repo
        self._uuid_generator = uuid_generator

    async def __call__(self, dto: NewBookDTO) -> str:
        uuid = str(self._uuid_generator())
        book = entities.BookDM(
            uuid=uuid,
            title=dto.title,
            pages=dto.pages,
            is_read=dto.is_read
        )

        await self._book_repo.save(book)
        await self._uow.commit()
        return uuid
