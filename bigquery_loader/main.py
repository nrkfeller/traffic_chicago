import logging

from big_query_getter import BigQueryGetter
from flask import Flask


app = Flask(__name__)


@app.route('/gettingdata')
def gettingdata():
    bqg = BigQueryGetter()
    bqg.get_region_data()
    bqg.get_segment_data()
    logging.info('Got data successfully')
    return 'success'


@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081, debug=True)
