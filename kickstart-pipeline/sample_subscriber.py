from concurrent.futures import TimeoutError

from google.cloud import pubsub_v1
import settings
import json

project_id = 'trhc-test'
subscription_id = 'kickstart-to-pipeline-sub'
timeout = 300.0

subscriber: pubsub_v1.SubscriberClient = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(project_id, subscription_id)


def callback(message):
    print(f"Secondary Message received {message}")
    print(json.loads(message.data))
    message.ack()


streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
print(f"Listening for messages on {subscription_path}...")

try:
    streaming_pull_future.result(timeout=timeout)
except TimeoutError:
    streaming_pull_future.cancel()
