import logging
import json
from big_query_getter import BigQueryGetter
from flask import Flask, Response


app = Flask(__name__)


@app.route('/gettingdata')
def gettingdata():
    bqg = BigQueryGetter()
    bqg.get_region_data()
    bqg.get_segment_data()
    logging.info('Got data successfully')
    return 'success'


@app.route('/segcoords')
def get_segcoords():

    data = json.load(open('segmentscoordinates.json'))

    js = json.dumps(data)
    resp = Response(js, status=200, mimetype='application/json')
    resp.headers['Link'] = 'mapsdata'

    return resp


@app.route('/regions')
def get_regions():

    data = json.load(open('regions.json'))

    js = json.dumps(data)
    resp = Response(js, status=200, mimetype='application/json')
    resp.headers['Link'] = 'mapsdata'

    return resp


@app.route('/segments')
def get_segments():

    data = json.load(open('segments.json'))

    js = json.dumps(data)
    resp = Response(js, status=200, mimetype='application/json')
    resp.headers['Link'] = 'mapsdata'

    return resp


@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
