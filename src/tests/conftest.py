import time

import docker
import pytest
from docker import APIClient

from service.consumer import QueueConsumer
from service.utils import connect_broker

TEST_RABBITMQ_IMAGE = "rabbitmq:3.12.8-alpine"
BROKER_HOST = "localhost"
QUEUE_NAME = "test"


def _get_health(container):
    """
    Inspect container and get the current health status.
    """
    api_client = APIClient()
    inspect_results = api_client.inspect_container(container.name)
    return inspect_results["State"]["Health"]["Status"]


@pytest.fixture(scope="session")
def rabbitmq_container():
    client = docker.from_env()

    rabbitmq = client.containers.run(
        image=TEST_RABBITMQ_IMAGE,
        detach=True,
        remove=True,
        ports={5672: 5672},
        name="test-rabbitmq",
        healthcheck={
            "test": "rabbitmq-diagnostics check_port_connectivity",
            "interval": 2000000000,
            "timeout": 3000000000,
            "retries": 30,
        },
    )

    while _get_health(rabbitmq) != "healthy":
        time.sleep(0.1)

    yield rabbitmq

    rabbitmq.stop(timeout=3)


@pytest.fixture(scope="session")
def rabbitmq_channel(rabbitmq_container):
    connection, channel = connect_broker(host=BROKER_HOST, queue=QUEUE_NAME)
    yield channel
    connection.close()


@pytest.fixture(scope="session")
def rabbitmq_consumer(rabbitmq_container):
    yield QueueConsumer(host=BROKER_HOST, queue=QUEUE_NAME, test_mode=True)
