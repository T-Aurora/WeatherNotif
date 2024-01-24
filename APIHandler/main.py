import sys
from WeatherProducer import WeatherProducer
from RedisCache import RedisCache
from Exporter import Exporter
from DataValutation import process_subs
import time
from confluent_kafka import KafkaException
import socket
import os
import json
#settare variabili d'ambiente su docker compose riguardo redis
def main():
    redis = RedisCache(os.getenv('REDIS_HOST','localhost'),os.getenv('REDIS_PORT','6379'),os.getenv('REDIS_DB','0'))
    weather_p=WeatherProducer(host=os.getenv('KAFKAHOST','localhost:29092'))
    exporter = Exporter()
    exporter.start_http_server()
    try:
        k_producer=weather_p.create_producer()
        while True:
            data = process_subs(redis)
            if data:
                for d in data:
                    print(d)
                    d = json.loads(d)
                    print("tipo d",type(d)) # tipo d <class 'dict'>
                    print(d['city'])
                    weather_p.send_data(producer=k_producer, topic='BakedData',data=d, key=d['city'])
                    city_name = d['city']
                    exporter.update_metrics(city_name)
            time.sleep(100)
    except KafkaException as e:
        if e.args[0].code() in (socket.errno.ECONNREFUSED,):
            print("Connection refused. Please check your Kafka broker.")
            sys.exit(1)
        else:
            print("Kafka error occurred:", e)

if __name__=="__main__":
    main()