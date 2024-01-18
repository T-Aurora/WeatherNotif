import redis
import json


class RedisLink:
    def __init__(self,host,port,db):
        self.redis_client = redis.Redis(host=host, port = port, db = db)
    def link_user(self,username,id):
        cached_data = self.redis_client.get(username)
        if cached_data:
            return "500"
        else:
            self.redis_client.set(username,id)
            return "200"