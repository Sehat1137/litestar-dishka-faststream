# litestar-dishka-faststream

This project is an implementation of "Clean architecture" in Python.

### Running the project

Install dependencies

```shell
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Run containers with rabbitMQ and PostgreSQL

```
cp .env.dist .env
docker compose up -d
```

Run migrations and creare queue

```shell
set -a
source .env
set +a
alembic upgrade head
docker exec -it book-club-rabbitmq rabbitmqadmin -u $RABBITMQ_USER -p $RABBITMQ_PASS -V / declare queue name=create_book durable=false
docker exec -it book-club-rabbitmq rabbitmqadmin -u $RABBITMQ_USER -p $RABBITMQ_PASS -V / declare queue name=book_statuses durable=false
```

Run the project

```shell
uvicorn --factory src.book_club.main:get_app --reload
```

Workflow 

```shell
// Publish message
docker exec -it book-club-rabbitmq rabbitmqadmin -u $RABBITMQ_USER -p $RABBITMQ_PASS \
publish exchange=amq.default routing_key=create_book payload='{"title": "The Brothers Karamazov", "pages": 928, "is_read": true}'

// Read uuid of created book
docker exec -it book-club-rabbitmq rabbitmqadmin -u $RABBITMQ_USER -p $RABBITMQ_PASS get queue=book_statuses count=1

// Get book info by http api
curl http://localhost:8000/book/{uuid}
```

Run only http
```shell
uvicorn --factory src.book_club.main:get_litestar_app --reload
```

Run only amqp
```shell
faststream --factory src.book_club.main:get_faststream_app --reload --host
```
