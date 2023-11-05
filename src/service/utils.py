import pika
import psycopg2
from psycopg2.extras import RealDictCursor


def connect_broker(host: str, queue: str) -> tuple:
    """
    Connect to the RabbitMQ broker and declare the queue. Returns connection and channel.
    """
    connection = pika.BlockingConnection(pika.ConnectionParameters(host))
    channel = connection.channel()
    channel.queue_declare(queue=queue)
    return connection, channel


def connect_database(host: str, dbname: str, user: str, password: str) -> tuple:
    """
    Connect to the Postgres database. Returns connection and cursor.
    """
    print("connection db")
    connection = psycopg2.connect(
        host=host, dbname=dbname, user=user, password=password
    )
    cursor = connection.cursor(cursor_factory=RealDictCursor)
    return connection, cursor
