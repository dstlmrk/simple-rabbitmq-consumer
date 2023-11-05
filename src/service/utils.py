import pika
from pika.adapters.blocking_connection import BlockingChannel, BlockingConnection


def connect_broker(host: str, queue: str) -> (BlockingConnection, BlockingChannel):
    """
    Connect to the RabbitMQ broker and declare the queue.
    """
    connection = pika.BlockingConnection(pika.ConnectionParameters(host))
    channel = connection.channel()
    channel.queue_declare(queue=queue)
    return connection, channel
