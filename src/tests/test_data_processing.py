import json

from utils import connect_broker, connect_database

from service.consumer import QueueConsumer

TEST_BROKER_PARAMS = dict(
    host="localhost",
    queue=(QUEUE_NAME := "test"),
)
TEST_DB_PARAMS = dict(
    host="localhost",
    dbname="parameters",
    user="user_name",
    password="user_password",
)


def test_real_dataset(offers):
    broker_connection, channel = connect_broker(**TEST_BROKER_PARAMS)
    db_connection, cursor = connect_database(**TEST_DB_PARAMS)

    # send them to queue
    for offer in offers:
        channel.basic_publish(
            exchange="", routing_key=QUEUE_NAME, body=json.dumps(offer).encode("utf-8")
        )

    # test own consumer
    QueueConsumer(
        broker_params=TEST_BROKER_PARAMS,
        db_params=TEST_DB_PARAMS,
        test_mode=True,
    ).run()

    cursor.execute("SELECT COUNT(*) FROM offer;")
    assert cursor.fetchone()["count"] == 5

    cursor.execute("SELECT * FROM offer;")
    for row, offer in zip(cursor.fetchall(), offers):
        assert row == {"id": offer["id"], **offer["legacy"]}

    cursor.execute("SELECT COUNT(*) FROM attribute;")
    assert cursor.fetchone()["count"] == 15

    cursor.execute("SELECT * FROM attribute;")
    for row, attr in zip(
        cursor.fetchall(),
        [
            {"offer_id": offer["id"], **attr}
            for offer in offers
            for attr in offer["attributes"] or []
        ],
    ):
        assert row == {
            "offerId": attr["offer_id"],
            "name": attr["name"],
            "value": attr["value"],
        }

    broker_connection.close()
    db_connection.close()
