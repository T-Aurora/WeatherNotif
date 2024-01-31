import os
from flask import jsonify
from prometheus_api_client import PrometheusConnect
class PrometheusRetriever:
    def __init__(self):
        self.prometheus_url = 'http://'+os.getenv('PROMETHEUSHOST','localhost:9090')
        self.prometheus = PrometheusConnect(url = self.prometheus_url, disable_ssl=True)

    def get_prometheus_metrics_latest_value(self,query):
        result = self.prometheus.get_current_metric_value(query)
        print(result)
        if result:
            #most_recent_result = max(result, key=lambda x: x['value'][0])
            value = result[-1]
            print("valore: ",value['value'])
            return value['value']
        else:
            return jsonify({'error': 'Query failed or no data returned'})
        #print(result)
        #return jsonify(result)


