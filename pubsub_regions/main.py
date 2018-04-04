import urllib
import json
import logging
from google.cloud import pubsub

from datetime import datetime
from pytz import timezone

from flask import Flask


app = Flask(__name__)

TRAFFIC_URL = 'https://data.cityofchicago.org/resource/t2qc-9pjd.json'
TOPIC = 'chicagoregions'
last_update = ''


def publish_to_pubsub(publisher, topic_path):
    global last_update

    response = urllib.urlopen(TRAFFIC_URL)
    data = json.loads(response.read())

    if last_update != data[0]['_last_updt']:

        last_update = data[0]['_last_updt']

        for entry in data:
            entry['current_speed'] = float(entry['current_speed'])
            entry['_east'] = float(entry['_east'])
            entry['_region_id'] = int(entry['_region_id'])
            entry['_north'] = float(entry['_north'])
            entry['_south'] = float(entry['_south'])
            entry['_west'] = float(entry['_west'])
            publisher.publish(
                topic_path,
                data=json.dumps(entry)
            )


def get_est_datetime():
    fmt = "%Y-%m-%d %H:%M:%S %Z%z"
    now_time = datetime.now(timezone('US/Eastern'))
    return now_time.strftime(fmt)


@app.route('/runreg')
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


TRAFFIC_URL_SEGMENTS = 'https://data.cityofchicago.org/resource/8v9j-bter.json'
TOPIC_SEGMENTS = 'chicagosegments'
last_update_seg = ''


def publish_segments_to_pubsub(publisher, topic_path):
    global last_update_seg

    response = urllib.urlopen(TRAFFIC_URL_SEGMENTS)
    data = json.loads(response.read())

    if last_update_seg != data[0]['_last_updt']:

        last_update_seg = data[0]['_last_updt']

        for entry in data:
            entry['_lif_lat'] = float(entry['_lif_lat'])
            entry['start_lon'] = float(entry['start_lon'])
            entry['_lit_lat'] = float(entry['_lit_lat'])
            entry['_traffic'] = float(entry['_traffic'])
            entry['_lit_lon'] = float(entry['_lit_lon'])
            entry['_length'] = float(entry['_length'])
            publisher.publish(
                topic_path,
                data=json.dumps(entry))


@app.route('/runseg')
def start_publishing_seg():
    print('get data')
    publisher = pubsub.PublisherClient()
    topic_path = publisher.topic_path('nickapi-184104', TOPIC_SEGMENTS)
    try:
        publisher.get_topic(topic_path)
        logging.info('Reusing pub/sub topic {}'.format(TOPIC_SEGMENTS))
    except:
        publisher.create_topic(topic_path)
        logging.info('Creating pub/sub topic {}'.format(TOPIC_SEGMENTS))
    publish_segments_to_pubsub(publisher, topic_path)
    return 'done'


if __name__ == '__main__':

    app.run(host='0.0.0.0', port=8080, debug=True)
