from typing import AsyncIterable
from uuid import uuid4

from dishka import Provider, Scope, provide, AnyOf, from_context
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from book_club.application import interfaces
from book_club.application.interactors import (
    GetBookInteractor,
    NewBookInteractor
)
from book_club.config import Config
from book_club.infrastructure.database import new_session_maker
from book_club.infrastructure.repository import BookRepository


class AppProvider(Provider):
    config = from_context(provides=Config, scope=Scope.APP)

    @provide(scope=Scope.APP)
    def get_uuid_generator(self) -> interfaces.UUIDGenerator:
        return uuid4

    @provide(scope=Scope.APP)
    def get_session_maker(self, config: Config) -> async_sessionmaker[AsyncSession]:
        return new_session_maker(config.postgres)

    @provide(scope=Scope.REQUEST)
    async def get_session(self, session_maker: async_sessionmaker[AsyncSession]) -> AsyncIterable[AnyOf[
        AsyncSession,
        interfaces.UoW,
    ]]:
        async with session_maker() as session:
            yield session

    @provide(scope=Scope.REQUEST)
    def get_book_repo(
            self,
            session: AsyncSession,
    ) -> AnyOf[
        interfaces.BookReader,
        interfaces.BookSaver,
    ]:
        return BookRepository(session)

    get_book_interactor = provide(GetBookInteractor, scope=Scope.REQUEST)
    create_new_book_interactor = provide(NewBookInteractor, scope=Scope.REQUEST)
