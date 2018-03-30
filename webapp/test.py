from google.cloud import storage
import json


def readFileFromBucket(filename):
    storage_client = storage.Client()

    bucket = storage_client.get_bucket('chicagobucket')
    blob = bucket.get_blob(filename)
    return json.loads(blob.download_as_string())


print(type(readFileFromBucket('regions.json')['Auburn Gresham-Chatham'][1][0]))
