import json
import os
from unittest.mock import call, patch


def test_broker(rabbitmq_channel, rabbitmq_consumer):
    with open(os.path.join(os.path.dirname(__file__), "mock_offers.json")) as file:
        offers = json.load(file)["offers"]

    for offer in offers:
        rabbitmq_channel.basic_publish(
            exchange="", routing_key="test", body=json.dumps(offer).encode("utf-8")
        )

    with patch("service.consumer.QueueConsumer.process_data") as mock_method:
        rabbitmq_consumer.run()

    assert mock_method.call_count == 5  # number of offers
    mock_method.assert_has_calls([call(offer) for offer in offers])
