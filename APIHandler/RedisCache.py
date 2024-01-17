import redis
import json
from WeatherData import fetch_weather_data
class RedisCache:
    def __init__(self,host,port,db):
        self.redis_client = redis.Redis(host=host, port = port, db = db)
    def get_cached_weather(self,city):
        cached_data = self.redis_client.get(city)
        if cached_data:
            return json.loads(cached_data)
        else:
            weather_data = fetch_weather_data(city)
            if weather_data:
                self.redis_client.setex(city,3600,json.dumps(weather_data))
            return weather_data
