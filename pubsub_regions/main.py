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
            publisher.publish(
                topic_path,
                data=get_est_datetime(),
                current_speed=entry['current_speed'].encode('utf-8'),
                _east=entry['_east'].encode('utf-8'),
                _last_updt=entry['_last_updt'].encode('utf-8'),
                _region_id=entry['_region_id'].encode('utf-8'),
                _north=entry['_north'].encode('utf-8'),
                _south=entry['_south'].encode('utf-8'),
                region=entry['region'].encode('utf-8'),
                _west=entry['_west'].encode('utf-8'),
                _description=entry['_description'].encode('utf-8')
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


if __name__ == '__main__':

    app.run(host='0.0.0.0', port=8080, debug=True)
