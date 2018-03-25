# beam gs text to gs text

import apache_beam as beam
import re

PROJECT = 'nickapi-184104'
BUCKET = 'mysb'


def run():
    argv = [
        '--project={0}'.format(PROJECT),
        '--job_name=examplejob2',
        '--save_main_session',
        '--staging_location=gs://{0}/staging/'.format(BUCKET),
        '--temp_location=gs://{0}/staging/'.format(BUCKET),
        '--runner=DataflowRunner'
    ]

    p = beam.Pipeline(argv=argv)

    inp = 'gs://{0}/test/kl.txt'.format(BUCKET)
    output_prefix = 'gs://{0}/test/output'.format(BUCKET)

    (p
        | beam.io.ReadFromText(inp)
        | beam.FlatMap(lambda x: re.findall(r'[A-Za-z\']+', x))
        | beam.combiners.Count.PerElement()
        | beam.Map(lambda word_count: '%s: %s' % (word_count[0],
                                                  word_count[1]))
        | beam.io.WriteToText(output_prefix)
     )

    p.run()


if __name__ == '__main__':
    run()
