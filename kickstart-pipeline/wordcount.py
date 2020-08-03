import logging
import re
import apache_beam as beam
from apache_beam.io import ReadFromText
from apache_beam.io import WriteToText
from apache_beam.options.pipeline_options import PipelineOptions
from settings import GCP_PROJECT, GCP_BUCKET_REGION, GCP_BUCKET_NAME


class CountWords(beam.PTransform):
    def expand(self, pcoll):
        return (
                pcoll
                # Convert lines of text into individual words.
                | 'ExtractWords' >>
                beam.FlatMap(lambda x: re.findall(r'[A-Za-z\']+', x))

                # Count the number of times each word occurs.
                | beam.combiners.Count.PerElement())


class FormatAsTextFn(beam.DoFn):
    def process(self, element):
        word, count = element
        yield '%s: %s' % (word, count)


options = PipelineOptions(
    ['--project', GCP_PROJECT, '--temp_location', f'{GCP_BUCKET_NAME}/tmp', '--region', GCP_BUCKET_REGION])


def run(argv=None):
    with beam.Pipeline(options=options) as p:
        lines = p | ReadFromText('gs://dataflow-samples/shakespeare/kinglear.txt')
        counts = lines | CountWords()
        output = counts | beam.ParDo(FormatAsTextFn())
        output | WriteToText(f'{GCP_BUCKET_NAME}/results/outputs')
        result = p.run()
        result.wait_until_finish()


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    run()
