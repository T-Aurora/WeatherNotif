from confluent_kafka import Producer, admin
from confluent_kafka.admin import NewTopic, AdminClient
import sys
import json
from WNotif_app import models
import time
import asyncio
import threading
#Random (adding some delay)
from random import randint
from time import sleep
#----
class KProducer:
    def __init__(self, broker):
        self.broker = broker
        self.conf = {'bootstrap.servers': self.broker}
        self.p = Producer(**self.conf)

    def delivery_callback(self, err, msg):
        if err:
            sys.stderr.write('%% Message failed delivery: %s\n' % err)
        else:
            sys.stderr.write('%% Message delivered to %s, partition[%d] @ %d\n' %
                             (msg.topic(), msg.partition(), msg.offset()))

        # p.produce(topic, key=record_key, value=record_value, callback=delivery_callback)

    def produce(self, app, data,topic):
        with app.app_context():
            print("Sub for weather_d", data)
            try:# 0 dopo no? no prima, vediamo se printa almeno l'username
                user = models.User.query.where(data["user_id"] == models.User.id).first()#credo forse data non ci arriva come json ma come stringa proprio
                print("Username: ",user.username)
                # Pubb il messaggio sul topic
                try:
                    self.p.produce(topic, key=data["city"], value=data, callback=self.delivery_callback)
                    # Attendere la conferma dell'invio
                    self.p.poll(0)
                except BufferError:
                    sys.stderr.write('%% Local producer queue is full: try again\n')
            except Exception as e:
                print(f"Exception in produce_weather_message: {e}")
                print("End of produce_weather_message")