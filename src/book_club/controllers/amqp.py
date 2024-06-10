from dishka.integrations.base import FromDishka as Depends
from faststream.rabbit import RabbitRouter

from src.book_club.application.dto import NewBookDTO
from src.book_club.application.interactors import NewBookInteractor
from src.book_club.controllers.schemas import BookSchema

AMQPBookController = RabbitRouter()


@AMQPBookController.subscriber("create_book")
@AMQPBookController.publisher("book_statuses")
async def handle(data: BookSchema, interactor: Depends[NewBookInteractor]) -> str:
    dto = NewBookDTO(
        title=data.title,
        pages=data.pages,
        is_read=data.is_read
    )
    uuid = await interactor(dto)
    return uuid
