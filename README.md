# Simple RabbitMQ consumer

The goal is parsing messages from a queue in RabbitMQ and store certain parts of them in a database.
The messages are JSON objects encoded in a binary format and represent an offer entity.
We need to extract the values under the keys `legacy` and `attributes` from the message and store them in the DB.

## RabbitMQ

I use the latest version of the simple message broker RabbitMQ based on Alpine Linux distribution (because of size).
If you need inspect the broker, visit `http://localhost:15672`. The queue is open on the default port `5672`.

## Postgres

There is Postgres which is based on Alpine. It uses the default port `5432`. The database schema
is loaded from `db/fixtures/init.sql`. For long-term data persistence is necessary to use docker volume.

I created two simple tables. In the first of them are offers stored. I expect that the number of legacy items
is static. The second table stores attributes. Maybe there could be better to store identification of products
than offers. But it depends on the data.

## Disclaimer

This code is not prepared for production environment. I don't care secured credentials, global configuration,
optimal settings of broker and database for real-world load, etc.

## It would be nice

- Add support for more workers
- Write more tests to verify the functionality of the broker (messages are read only once etc.)
- Think about [asynchronous code](https://aio-pika.readthedocs.io/en/latest/rabbitmq-tutorial/1-introduction.html)
- Add pre-commit hook and don't use `ruff --fix . && isort . && black .` 🙂
- Better test parametrization (do not load all data in one test)
- Test broker and database separately
- Write idempotent tests (wrap up them by transactions)

## How to use

1. Install docker and docker-compose
2. Then run `docker compose up`
3. For testing on your machine, install and run `pytest` (step 2 is required)
4. Finally `docker compose down`
