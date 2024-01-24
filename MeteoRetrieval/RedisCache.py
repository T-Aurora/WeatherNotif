import redis
import json
from WeatherData import fetch_weather_data
from prometheus_client import Counter
from Exporter import Exporter

class RedisCache:
    def __init__(self,host,port,db):
        self.redis_client = redis.Redis(host=host, port = port, db = db)
        self.ex=Exporter()
    def get_cached_weather(self,city):
        cached_data = self.redis_client.get(city)
        if cached_data:
            #self.ex.cache_hit_counter.inc()
            self.ex.cache_hit_counter.labels(city=city).inc()
            return json.loads(cached_data)
        else:
            #counter di call api
            #self.ex.cache_miss_counter.inc()
            self.ex.cache_miss_counter.labels(city=city).inc()
            weather_data = fetch_weather_data(city)
            if weather_data:
                self.redis_client.setex(city,3600,json.dumps(weather_data))
            return weather_data