from __future__ import absolute_import

import logging
import argparse
import apache_beam as beam

'''Normalize pubsub string to json object'''
# Lines look like this:
# {'datetime': '2017-07-13T21:15:02Z', 'mac': 'FC:FC:48:AE:F6:94', 'status': 1}

PROJECT = 'nickapi-184104'
BUCKET = 'mysb'


def parse_pubsub(line):
    import json
    record = json.loads(line)
    return (record['_direction']), (record['_fromst']), (record['_traffic'])


def run(argv=None):

    pipeline_args = [
        '--project={0}'.format(PROJECT),
        '--job_name=pubsubtobq',
        '--runner=DataflowRunner',
        '--streaming',
        '--staging_location=gs://{0}/staging/'.format(BUCKET),
        '--temp_location=gs://{0}/staging/'.format(BUCKET),
    ]

    with beam.Pipeline(argv=pipeline_args) as p:
        # Read the pubsub topic into a PCollection.
        lines = (p | beam.io.ReadStringsFromPubSub('projects/nickapi-184104/topics/chicago')
                 | beam.Map(parse_pubsub)
                 | beam.Map(lambda (d, f, t): {'direction': d, 'fromst': f, 'traffic': t})
                 | beam.io.WriteToBigQuery(
            table='nickapi-184104:demos.streamdemo',
            schema=' direction:STRING, fromtst:INTEGER, traffic:TIMESTAMP',
            create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
            write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND)
        )


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    run()
