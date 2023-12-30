from confluent_kafka import Producer, admin
from confluent_kafka.admin import NewTopic, AdminClient
import sys
import json
from WNotif_app import models
import time
import asyncio
import threading
from ApiHandler import WeatherCall

#Random (adding some delay)
from random import randint
from time import sleep
from ApiHandler import WeatherCall
#----
class ProducerW:
    def __init__(self, app):
        self.broker = 'kafka'
        self.conf = {'bootstrap.servers': self.broker}
        self.p = Producer(**self.conf)
        self.topic_name = "WAlerts"
        self.topic_config = {
        'num_partitions': 3,  # Number of partitions
        'replication_factor': 1  # Replication factor (set according to your cluster config)
        }
        self.topic = NewTopic(self.topic_name, **self.topic_config)
        self.admin_client = AdminClient({'bootstrap.servers': self.broker})
        try:
            fs = self.admin_client.create_topics([self.topic])
            # Wait for each operation to finish.
            for topic, f in fs.items():
                try:
                        f.result()  # The result itself is None
                        print(f"Topic {topic} created")
                except Exception as e:
                        print(f"Failed to create topic {topic}: {e}")
        except Exception as e:
            print(f"Failed to create topic {self.topic_name}: {e}")
        self.app = app

    def delivery_callback(self, err, msg):
        if err:
            sys.stderr.write('%% Message failed delivery: %s\n' % err)
        else:
            sys.stderr.write('%% Message delivered to %s, partition[%d] @ %d\n' %
                             (msg.topic(), msg.partition(), msg.offset()))

        # p.produce(topic, key=record_key, value=record_value, callback=delivery_callback)
    def produce_weather_message(self,app):
        with app.app_context():
            while True:
                #region
                #WeatherCall
                try:
                    print("Ti entro nel try del producer!")
                    all_sub = models.Subscription.query.all()  #da gestire ritorno vuoto
                    if all_sub:
                        print("Ti entro nel if all_sub del producer!")
                    #for city in x['ciry]
                        for sub in all_sub:
                                cond = False
                                sub_city=sub.locazione
                                print("Sub for city", sub_city)
                                sub_weather_data=WeatherCall(sub_city)
                                print("Sub for weather_d", sub_weather_data)
                                chat_id = models.User.query.join(models.Subscription).where(sub.user_id == models.User.id).first()
                                print(chat_id.chat_id)
                                msg_data={
                                    'city':sub_city,
                                    'chat_id': chat_id.chat_id
                                }
                                print("Stampo il msg_data: ", msg_data)
                                #check su temp se c'è piopggia fai produc
                                print(sub.w_condition)
                                print(sub_weather_data['weather'][0]['id'] )
                                if sub.w_condition == 'rain' and sub_weather_data['weather'][0]['id'] == 500:
                                    msg_data['rain'] = 'It\'s gonna rain'
                                    cond = True
                                    print(f"Condition 1: {sub.w_condition == 'rain' and sub_weather_data['weather'][0]['id'] == 500}")

                                if sub.t_max and sub.t_max <= sub_weather_data['main']['temp_max']:
                                    msg_data['max_temp'] = 'the temperature is going to get as high as:  '+str(sub_weather_data['main']['temp_max'])
                                    cond = True
                                    print(f"Condition 2: {sub.t_max and sub.t_max <= sub_weather_data['main']['temp_max']}")

                                if sub.t_min and sub.t_min >= sub_weather_data['main']['temp_min']:
                                    msg_data['min_temp'] = 'the temperature is going to get as low as:  '+str(sub_weather_data['main']['temp_min'])
                                    cond = True
                                    print(f"Condition 3: {sub.t_min and sub.t_min >= sub_weather_data['main']['temp_min']}")
                                if cond:
                                    record_value = json.dumps(msg_data)
                                    # Pubb il messaggio sul topic
                                    topic = 'WAlerts'
                                    self.p.produce(topic ,key=chat_id.chat_id, value=record_value, callback=self.delivery_callback)
                                    # Attendere la conferma dell'invio
                                    self.p.poll(0)

                    else:
                        print("No subscriptions")
                except BufferError:
                    sys.stderr.write('%% Local producer queue is full: try again\n')
                except Exception as e:
                    print(f"Exception in produce_weather_message: {e}")
                    print("End of produce_weather_message")
                finally:
                    time.sleep(120)