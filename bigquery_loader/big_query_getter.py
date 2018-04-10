from google.cloud import bigquery
from google.cloud import storage
from collections import defaultdict

import logging
import json

BUCKET_NAME = 'chicagobucket'


class BigQueryGetter(object):
    def __init__(self):
        self.client = bigquery.Client()

    def get_region_data(self):
        client = bigquery.Client()

        query_job = client.query(
            """
            SELECT _last_updt, current_speed, region
            FROM `nickapi-184104.demos.regions`
            Order by _last_updt desc
            LIMIT 2700
        """
        )

        iterator = query_job.result()

        region_speed = defaultdict(list)
        region_time = defaultdict(list)

        for i in iterator:
            region_speed[i['region']].append(i['current_speed'])
            region_time[i['region']].append(str(i['_last_updt']))

        output = dict()

        for key in region_speed.keys():
            output[key] = [region_speed[key], region_time[key]]

        filename = 'regions.json'

        with open(filename, 'w') as outfile:
            json.dump(output, outfile)

        self._upload_blob(BUCKET_NAME, filename, filename)

        logging.info("{} uploaded to {}".format(filename, BUCKET_NAME))

    def get_segment_data(self):
        query_job = self.client.query(
            """
      SELECT
        _last_updt,
        segmentid,
        _traffic,
        street,
        _lif_lat,
        start_lon,
        _lit_lat,
        _lit_lon
      FROM `nickapi-184104.demos.segments`
      ORDER BY
        _last_updt desc
      LIMIT 824
      """
        )

        iterator = query_job.result()
        rows = list(iterator)

        output = {}
        output['_last_updt'] = []
        output['segmentid'] = []
        output['_traffic'] = []

        segments_map = dict()

        for row in rows:
            output['_last_updt'].append(str(row['_last_updt']))
            output['segmentid'].append(row['segmentid'])
            output['_traffic'].append(row['_traffic'])

            segments_map[row['street']] = [
                [row['_lif_lat'], row['start_lon']],
                [row['_lit_lat'], row['_lit_lon']]
            ]

        filename = 'segmentscoordinates.json'
        with open(filename, 'w') as outfile:
            json.dump(segments_map, outfile)

        self._upload_blob(BUCKET_NAME, filename, filename)

        filename = 'segments.json'

        with open(filename, 'w') as outfile:
            json.dump(output, outfile)

        self._upload_blob(BUCKET_NAME, filename, filename)

        logging.info("{} uploaded to {}".format(filename, BUCKET_NAME))

    def _upload_blob(self,
                     bucket_name,
                     source_file_name,
                     destination_blob_name):
        """Uploads a file to the bucket."""
        storage_client = storage.Client()
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)

        blob.upload_from_filename(source_file_name)

        print('File {} uploaded to {}.'.format(
            source_file_name,
            destination_blob_name))
