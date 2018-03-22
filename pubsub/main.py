import urllib
import json
import logging
from google.cloud import pubsub

from datetime import datetime
from pytz import timezone

from flask import Flask


app = Flask(__name__)

TRAFFIC_URL = 'https://data.cityofchicago.org/resource/8v9j-bter.json'
TOPIC = 'chicago'
last_update = ''


def publish_to_pubsub(publisher, topic_path):
    global last_update

    response = urllib.urlopen(TRAFFIC_URL)
    data = json.loads(response.read())

    if last_update != data[0]['_last_updt']:

        print('new batch')

        last_update = data[0]['_last_updt']

        for entry in data:
            publisher.publish(
                topic_path,
                data=get_est_datetime(),
                _direction=entry['_direction'].encode('utf-8'),
                _fromst=entry['_fromst'].encode('utf-8'),
                _last_updt=entry['_last_updt'].encode('utf-8'),
                _length=entry['_length'].encode('utf-8'),
                _lif_lat=entry['_lif_lat'].encode('utf-8'),
                _lit_lat=entry['_lit_lat'].encode('utf-8'),
                _lit_lon=entry['_lit_lon'].encode('utf-8'),
                _strheading=entry['_strheading'].encode('utf-8'),
                _tost=entry['_tost'].encode('utf-8'),
                _traffic=entry['_traffic'].encode('utf-8'),
                segmentid=entry['segmentid'].encode('utf-8'),
                start_lon=entry['start_lon'].encode('utf-8'),
                street=entry['street'].encode('utf-8'),
            )


def get_est_datetime():
    fmt = "%Y-%m-%d %H:%M:%S %Z%z"
    now_time = datetime.now(timezone('US/Eastern'))
    return now_time.strftime(fmt)


@app.route('/')
def start_publishing():
    print('get data')
    publisher = pubsub.PublisherClient()
    topic_path = publisher.topic_path('nickapi-184104', TOPIC)
    try:
        publisher.get_topic(topic_path)
        logging.info('Reusing pub/sub topic {}'.format(TOPIC))
    except:
        publisher.create_topic(topic_path)
        logging.info('Creating pub/sub topic {}'.format(TOPIC))
    publish_to_pubsub(publisher, topic_path)
    return 'done'


if __name__ == '__main__':

    app.run(host='127.0.0.1', port=8080, debug=True)
