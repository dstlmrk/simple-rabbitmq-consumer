import logging
import os

from consumer import QueueConsumer

BROKER_PARAMS = dict(
    host=os.environ["BROKER_HOST"],
    queue=os.environ["BROKER_QUEUE"],
)
DB_PARAMS = dict(
    host=os.environ["DB_HOST"],
    dbname=os.environ["DB_NAME"],
    user=os.environ["DB_USER"],
    password=os.environ["DB_PASSWORD"],
)


if __name__ == "__main__":
    try:
        consumer = QueueConsumer(
            broker_params=BROKER_PARAMS,
            db_params=DB_PARAMS,
            test_mode=False,
        )
        consumer.run()
    except Exception:
        logging.error("Unexpected error")
        raise
