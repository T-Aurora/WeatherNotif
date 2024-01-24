import logging
import os
import socket
import time
import prometheus_client
from prometheus_client import Counter


class Exporter:
    cache_hit_counter = Counter('cache_hits', 'Cache Hit Count',['city'])
    cache_miss_counter = Counter('cache_misses', 'Cache Miss Count',['city'])
    def __init__(self, port=9999, update_period=30):
        self.port = int(os.environ.get('PORT', port))
        self.update_period = update_period


    def start_http_server(self):
        prometheus_client.start_http_server(self.port)
        logging.basicConfig(level=logging.INFO, handlers=[logging.StreamHandler()])
        logging.info('Starting exporter on port %s', self.port)
        logging.info('metric path: /metrics')

    def update_metrics(self, city):
        cache_hit_value = self.cache_hit_counter.labels(city=city)._value.get()
        cache_miss_value = self.cache_miss_counter.labels(city=city)._value.get()
        #cache_hit_value = self.cache_hit_counter._value.get()
        #cache_miss_value = self.cache_miss_counter._value.get()
        logging.info('Cache Hit Count for %s: %s', city, cache_hit_value)
        logging.info('Cache Miss Count for %s: %s', city, cache_miss_value)
        #logging.info('Cache Hit Count: %s', cache_hit_value)
        #logging.info('Cache Miss Count: %s', cache_miss_value)
