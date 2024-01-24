import sys

from confluent_kafka import Producer
import time
import json

class WeatherProducer:
    def __init__(self,host):
        self.kafka_config = {
            'bootstrap.servers':host
        }
    def delivery_callback(self, err, msg):
        if err:
            sys.stderr.write('%% Message failed delivery: %s\n' % err)
        else:
            sys.stderr.write('%% Message delivered to %s, partition[%d] @ %d\n' %
                             (msg.topic(), msg.partition(), msg.offset()))
    def create_producer(self):
        return Producer(self.kafka_config)

    def send_data(self,producer,topic,data,key):
        producer.produce(topic = topic,key = key, value = json.dumps(data).encode('utf-8'), callback=self.delivery_callback)

