import logging
import apache_beam as beam
from apache_beam.io import WriteToText
from apache_beam.options.pipeline_options import PipelineOptions
from settings import GCP_PROJECT, GCP_BUCKET_REGION, GCP_BUCKET_NAME, TOPIC, brew_db_url, BREWERY_DB_API_KEY
import requests
import json

Beer = {
    'name': str,
    'description': str,
    'id': str,
    'style': str,
    'quantity': int,
}


class GetDescription(beam.DoFn):
    def process(self, element):
        beer: Beer = json.loads(element)
        response = requests.get(f"{brew_db_url}/beers", params={'key': BREWERY_DB_API_KEY, 'name': beer['name']})
        body = response.json()
        description = 'none found'
        if body['totalResults'] > 0:
            if 'description' in body['data'][0]:
                description = body['data'][0]['description']
            elif 'style' in body['data'][0]:
                description = body['data'][0]['style']['description']
        yield json.dumps({**beer, 'description': description})


def run(pipeline_args=None):
    pipeline_options = PipelineOptions(
        pipeline_args, streaming=True, save_main_session=True, project=GCP_PROJECT, region=GCP_BUCKET_REGION,
        runner='DataflowRunner', temp_location=f'{GCP_BUCKET_NAME}/tmp', experiments=["allow_non_updatable_job"]
    )
    with beam.Pipeline(options=pipeline_options) as pipeline:
        (
                pipeline
                | "Read PubSub Messages"
                >> beam.io.ReadFromPubSub(topic=TOPIC)
                | "Get Description From Brew DB" >> beam.ParDo(GetDescription())
                | WriteToText(f'{GCP_BUCKET_NAME}/test-topic/outputs')
        )


if __name__ == "__main__":  # noqa
    logging.getLogger().setLevel(logging.INFO)
    run()
