import os
import sys
from confluent_kafka import Consumer, KafkaException
import socket
import json
from time import sleep
from KProducer import KProducer
import time

class KExchange:
    def __init__(self,topic):
        self.c = Consumer({'bootstrap.servers': os.getenv('KAFKAHOST','localhost:29092'),
                      'group.id': 1,
                      'enable.auto.commit': 'true',
                      'auto.offset.reset': 'latest',  # 'auto.offset.reset=earliest' to start reading from the beginning - [latest, earliest, none]
                      })
        self.c.subscribe([topic])
        try:
            self.producer = KProducer(os.getenv('KAFKAHOST','localhost:29092'))
        except KafkaException as e:
            if e.args[0].code() in (socket.errno.ECONNREFUSED,):
                print("Connection refused. Please check your Kafka broker.")
                sys.exit(1)

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
                    print(msg.key(),msg.value())
                    print(record_value)
                    print("Consumed record with key {} and value {}".format(record_key, record_value))
                    #produce message al topic WAlerts con i dati presi, creare funziona su KProducer, inviare dati "baked"
                    self.producer.produce(app,record_value,'WAlerts')
        except KeyboardInterrupt:
            pass
        finally:
            # Leave group and commit final offsets
            self.c.close()