import logging

from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    arr = [1, 2, 3]
    return render_template('index.html', value=arr)


@app.route('/architecture')
def architecture():
    """Return a friendly HTTP greeting."""
    return render_template('architecture.html')


@app.route('/dashboard')
def dashboard():
    """Return a friendly HTTP greeting."""
    return render_template('dashboard.html')


@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500


if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END app]
