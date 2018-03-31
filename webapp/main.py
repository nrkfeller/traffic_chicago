from google.cloud import storage

import logging
import json
import urllib

from flask import Flask, render_template

app = Flask(__name__)

SEGMENTS_BLOB = 'segments.json'
REGIONS_BLOB = 'regions.json'
SEGMENTS_URL = \
    'https://gettingdatatogs-dot-nickapi-184104.appspot.com/segments'
REGIONS_URL = \
    'https://gettingdatatogs-dot-nickapi-184104.appspot.com/regions'


@app.route('/')
def hello():
    response = urllib.urlopen(SEGMENTS_URL)
    data = json.loads(response.read())
    return render_template('index.html', segments=data)


@app.route('/architecture')
def architecture():
    return render_template('architecture.html')


@app.route('/dashboard')
def dashboard():
    response = urllib.urlopen(SEGMENTS_URL)
    segments = json.loads(response.read())

    response = urllib.urlopen(REGIONS_URL)
    regions = json.loads(response.read())

    return render_template('dashboard.html',
                           regions=regions,
                           segments=segments
                           )


@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500


def readFileFromBucket(filename):
    storage_client = storage.Client()

    bucket = storage_client.get_bucket('chicagobucket')
    blob = bucket.get_blob(filename)
    return json.loads(blob.download_as_string())


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END app]
