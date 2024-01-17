from WeatherProducer import WeatherProducer
from RedisCache import RedisCache
import os
#settare variabili d'ambiente su docker compose riguardo redis
def main():
    redis = RedisCache(os.getenv('REDIS_HOST','localhost'),os.getenv('REDIS_PORT','6379'),os.getenv('REDIS_DB','0'))
    weather_p=WeatherProducer(host='localhost')
    k_producer=weather_p.create_producer()
    #call all_sub
    #scorrere sub con for, per ogni citta della sub fare get_cached_w.. poi produrre il msg con i dati di opw e dati utenti con user id
    #dato combo con dati opw e dati redis e valutazione dei dati ed avvertire questo utente 
    weather_p.send_data(producer=k_producer, topic='WAlert',data=redis.get_cached_weather())


if __name__=="__main__":
    main()