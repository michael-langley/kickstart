from dotenv import load_dotenv
import os

load_dotenv()

GCP_BUCKET_NAME = os.getenv("GCP_BUCKET_NAME")
GCP_BUCKET_REGION = os.getenv("GCP_BUCKET_REGION")
GCP_PROJECT = os.getenv("GCP_PROJECT")
PUB_SUB_OUTGOING_TOPIC = os.getenv("PUB_SUB_OUTGOING_TOPIC")
