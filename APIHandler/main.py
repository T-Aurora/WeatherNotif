from WeatherProducer import WeatherProducer
from RedisCache import RedisCache
from DataValutation import process_subs
import time
import os
#settare variabili d'ambiente su docker compose riguardo redis
def main():
    redis = RedisCache(os.getenv('REDIS_HOST','localhost'),os.getenv('REDIS_PORT','6379'),os.getenv('REDIS_DB','0'))
    weather_p=WeatherProducer(host=os.getenv('KAFKAHOST','localhost:29092'))
    k_producer=weather_p.create_producer()
    while True:
        weather_p.send_data(producer=k_producer, topic='BakedData',data=process_subs(redis))
        time.sleep(60)

if __name__=="__main__":
    main()