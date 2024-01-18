import os

from confluent_kafka import Consumer
import json
from time import sleep
from KProducer import KProducer

MIN_COMMIT_COUNT = 4
class KExchange:
    def commit_completed(err, partitions):
        if err:
            print(str(err))
        else:
            print("Committed partition offsets: " + str(partitions))
    def __init__(self,topic):
        self.c = Consumer({'bootstrap.servers': 'localhost:29092',
                      'group.id': 1,
                      'enable.auto.commit': 'true',
                      'auto.offset.reset': 'latest',  # 'auto.offset.reset=earliest' to start reading from the beginning - [latest, earliest, none]
                      })
        self.c.subscribe([topic])
        self.producer = KProducer(os.getenv('KAFKAHOST','localhost:29092'))

    def consume(self):
        try:
            while True:
                msg = self.c.poll(timeout=5.0)
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
                    count = data['count']
                    print("Consumed record with key {} and value {}".format(record_key, record_value))
                    #produce message al topic WAlerts con i dati presi, creare funziona su KProducer, inviare dati "baked"

        except KeyboardInterrupt:
            pass
        finally:
            # Leave group and commit final offsets
            self.c.close()