import os
from confluent_kafka import Consumer
import json
from time import sleep
from KProducer import KProducer
import time

class KExchange:
    def __init__(self,topic):
        self.c = Consumer({'bootstrap.servers': 'localhost:29092',
                      'group.id': 1,
                      'enable.auto.commit': 'true',
                      'auto.offset.reset': 'latest',  # 'auto.offset.reset=earliest' to start reading from the beginning - [latest, earliest, none]
                      })
        self.c.subscribe([topic])
        self.producer = KProducer(os.getenv('KAFKAHOST','localhost:29092'))

    def ConsumeandProduce(self,app):
        try:
            while True:
                msg = self.c.poll(timeout=10.0)
                if msg is None:
                    print("Waiting for message or event/error in poll()")
                    continue
                elif msg.error():
                    print('error: {}'.format(msg.error()))
                else:
                    # Check for Kafka message
                    record_key = msg.key()
                    record_value = msg.value()
                    data = json.loads(record_value)
                    print(data)
                    print("Consumed record with key {} and value {}".format(record_key, data))
                    #produce message al topic WAlerts con i dati presi, creare funziona su KProducer, inviare dati "baked"
                    self.producer.produce(app,data,'WAlerts')
                time.sleep(30)
        except KeyboardInterrupt:
            pass
        finally:
            # Leave group and commit final offsets
            self.c.close()