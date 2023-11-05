import json
import os

import pytest


@pytest.fixture(scope="session")
def offers():
    """
    Load offers from real dataset.
    """
    with open(os.path.join(os.path.dirname(__file__), "mock_offers.json")) as file:
        offers = json.load(file)["offers"]
    return offers
