import json

from utils import connect_broker


class QueueConsumer:
    def __init__(self, host: str, queue: str, test_mode: bool = False):
        self.queue = queue
        self.test_mode = test_mode
        _, self.channel = connect_broker(host, queue)

    def process_data(self, data):
        """
        Process data from a queue and store certain parts of them in a database.
        """
        pass

    def run(self):
        """
        Start consuming from message broker. For testing purposes,
        the method enables to stop consuming when the queue is empty.
        """
        print("Start consuming...")
        for method, _, body in self.channel.consume(
            queue=self.queue, auto_ack=False, inactivity_timeout=1
        ):
            if not body:
                if self.test_mode:
                    return
                else:
                    continue

            self.process_data(json.loads(body))
            # Confirm the message is processed
            self.channel.basic_ack(method.delivery_tag)
