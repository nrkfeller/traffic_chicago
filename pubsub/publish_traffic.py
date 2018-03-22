import urllib
import json
import logging
import time
from google.cloud import pubsub

TRAFFIC_URL = 'https://data.cityofchicago.org/resource/8v9j-bter.json'
TOPIC = 'chicago'
last_update = ''


def publish_to_pubsub(publisher, topic_path):
    global last_update

    response = urllib.urlopen(TRAFFIC_URL)
    data = json.loads(response.read())

    if last_update != data[0]['_last_updt']:

        print 'new batch'

        last_update = data[0]['_last_updt']

        for entry in data:
            publisher.publish(
                topic_path,
                data=entry['segmentid'].encode('utf-8'),
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


def start_publishing(publisher, topic_path):
    while True:
        publish_to_pubsub(publisher, topic_path)
        time.sleep(5)


if __name__ == '__main__':
    publisher = pubsub.PublisherClient()
    topic_path = publisher.topic_path('nickapi-184104', TOPIC)
    try:
        publisher.get_topic(topic_path)
        logging.info('Reusing pub/sub topic {}'.format(TOPIC))
    except:
        publisher.create_topic(topic_path)
        logging.info('Creating pub/sub topic {}'.format(TOPIC))
    start_publishing(publisher, topic_path)
