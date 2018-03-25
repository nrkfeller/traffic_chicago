import apache_beam as beam
import six
import re
import sys

if __name__ == '__main__':
    p = beam.Pipeline(argv=sys.argv)

    (p
        | beam.io.ReadFromText('kl.txt')
        | beam.FlatMap(lambda x: re.findall(r'[A-Za-z\']+', x))
        | beam.combiners.Count.PerElement()
        | beam.Map(lambda word_count: '%s: %s' % (word_count[0],
                                                  word_count[1]))
        | beam.io.WriteToText('out.txt')
     )

    result = p.run()
    result.wait_until_finish()
