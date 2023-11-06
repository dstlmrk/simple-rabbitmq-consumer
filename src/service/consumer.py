import json
import logging

from utils import connect_broker, connect_database


class QueueConsumer:
    def __init__(self, broker_params: dict, db_params: dict, test_mode: bool = False):
        self.broker_connection, self.channel = connect_broker(**broker_params)
        self.queue = broker_params["queue"]
        self.db_connection, self.cursor = connect_database(**db_params)
        self.test_mode = test_mode

    def stop(self):
        """
        Close all connections
        """
        logging.info("Stop consuming...")
        self.broker_connection.close()
        self.cursor.close()
        self.db_connection.close()

    def process_data(self, data):
        """
        Process data from a queue and store certain parts of them in a database.
        """
        offer_id = data["id"]

        self.cursor.execute(
            """
            INSERT INTO offer (id, "platformId", "countryCode", "platformSellerId", "platformOfferId",
            "platformProductId", "isOversizeDelivery", "isDeliveryFeeByQuantity", "unitWeightGram",
            "isFreeMarketplaceDelivery") VALUES (%(id)s, %(platformId)s, %(countryCode)s,
            %(platformSellerId)s, %(platformOfferId)s, %(platformProductId)s, %(isOversizeDelivery)s,
            %(isDeliveryFeeByQuantity)s, %(unitWeightGram)s,%(isFreeMarketplaceDelivery)s)
            ON CONFLICT DO NOTHING
            """,
            {"id": offer_id, **data["legacy"]},
        )

        for attribute in data["attributes"] or []:
            self.cursor.execute(
                """
                INSERT INTO attribute ("offerId", name, value)
                VALUES (%s, %s, %s) ON CONFLICT DO NOTHING
                """,
                (offer_id, attribute["name"], attribute["value"]),
            )

        self.db_connection.commit()

    def run(self):
        """
        Start consuming from the message broker. For testing purposes,
        the method enables to stop consuming when the queue is empty.
        """
        logging.info("Start consuming...")
        for method, _, body in self.channel.consume(
            queue=self.queue, auto_ack=False, inactivity_timeout=1
        ):
            if body:
                self.process_data(json.loads(body))
                # Confirm the message is processed
                self.channel.basic_ack(method.delivery_tag)
            elif self.test_mode:
                self.stop()
