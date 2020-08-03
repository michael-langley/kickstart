from dotenv import load_dotenv
import os

load_dotenv()

GCP_BUCKET_NAME = os.getenv("GCP_BUCKET_NAME")
GCP_BUCKET_REGION = os.getenv("GCP_BUCKET_REGION")
GCP_PROJECT = os.getenv("GCP_PROJECT")
TOPIC = os.getenv('TOPIC')
BREWERY_DB_API_KEY = os.getenv("BREWERY_DB_API_KEY")
brew_db_url = "https://sandbox-api.brewerydb.com/v2/"
