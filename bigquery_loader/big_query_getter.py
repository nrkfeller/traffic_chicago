from google.cloud import bigquery
from google.cloud import storage

import logging
import pickle

BUCKET_NAME = 'chicagobucket'


class BigQueryGetter(object):
    def __init__(self):
        self.client = bigquery.Client()

    def get_segment_data(self):
        regions_query = """
        SELECT DISTINCT
          region
        FROM
          `nickapi-184104.demos.regions`
        """
        query_job = self.client.query(regions_query)

        rows = query_job.result()

        regions = [str(row['region']) for row in rows]

        query = """
        SELECT
            _last_updt, current_speed
        FROM
        `nickapi-184104.demos.regions`
        WHERE
            region=@REGION
        ORDER BY
            _last_updt
        """

        output = dict()
        for region in regions:

            query_params = [
                bigquery.ScalarQueryParameter('REGION', 'STRING', region)
            ]
            job_config = bigquery.QueryJobConfig()
            job_config.query_parameters = query_params
            query_job = self.client.query(query, job_config=job_config)

            rows = query_job.result()

            times = []
            speeds = []
            for row in rows:
                times.append(row['_last_updt'])
                speeds.append(row['current_speed'])

            output[region] = [times, speeds]

        filename = 'segments.pickle'

        with open(filename, 'wb') as handle:
            pickle.dump(output, handle, protocol=pickle.HIGHEST_PROTOCOL)

        self._upload_blob(BUCKET_NAME, filename, filename)

    def get_region_data(self):
        query_job = self.client.query(
            """
      SELECT _last_updt, segmentid, _traffic
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

        for row in rows:
            output['_last_updt'].append(row['_last_updt'])
            output['segmentid'].append(row['segmentid'])
            output['_traffic'].append(row['_traffic'])

        filename = 'regions.pickle'

        with open(filename, 'wb') as handle:
            pickle.dump(output, handle, protocol=pickle.HIGHEST_PROTOCOL)

        self._upload_blob(BUCKET_NAME, filename, filename)

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
