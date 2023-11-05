import logging
import os

from consumer import QueueConsumer

BROKER_HOST = os.environ["BROKER_HOST"]
QUEUE_NAME = os.environ["QUEUE_NAME"]


if __name__ == "__main__":
    try:
        consumer = QueueConsumer(BROKER_HOST, QUEUE_NAME)
        consumer.run()
    except Exception:
        logging.error("Unexpected error")
        raise
