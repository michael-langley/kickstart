from google.cloud import pubsub_v1

from models.beer import Beer
from settings import GCP_PROJECT, PUB_SUB_OUTGOING_TOPIC

publisher: pubsub_v1.PublisherClient = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(GCP_PROJECT, PUB_SUB_OUTGOING_TOPIC)


def send_notification(beer: Beer):
    data = beer.to_publishable.encode("utf-8")
    future = publisher.publish(topic_path, data=data)
    print(f"Notification sent {future.result}")
