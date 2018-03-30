from google.cloud import storage

import logging
import json

from flask import Flask, render_template

app = Flask(__name__)

SEGMENTS_BLOB = 'segments.json'
REGIONS_BLOB = 'regions.json'


@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    #regions = readFileFromBucket(REGIONS_BLOB)
    arr = [1, 2, 3]
    return render_template('index.html', value=arr)


@app.route('/architecture')
def architecture():
    """Return a friendly HTTP greeting."""
    return render_template('architecture.html')


@app.route('/dashboard')
def dashboard():
    """Return a friendly HTTP greeting."""
    segments = readFileFromBucket(SEGMENTS_BLOB)
    regions = readFileFromBucket(REGIONS_BLOB)

    # dt = regions['Downtown Lakefront']
    # values = reversed(dt[0][-20:])
    # times = reversed([str(i) for i in dt[1]][-20:])

    return render_template('dashboard.html',
                           regions=json.dumps(regions),
                           segments=json.dumps(segments)
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
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END app]
