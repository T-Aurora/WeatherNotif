import threading
import time
from PrometheusRetrieval import PrometheusRetriever


class ViolationChecker:
    def __init__(self):
        self.prometheus_retriever=PrometheusRetriever()

    def check_violations(self,db):
        while True:
            metrics = db.Model.SLAMetric.query.all()
            if metrics:
                for metric in metrics:
                    current_metric = self.prometheus_retriever.get_prometheus_metrics_latest_value(metric.name)
                    metric.current_value = current_metric[1]
                    if  metric.current_value > metric.desired_value:
                        print("Violation detected!")
                        metric.violation = True
                        metric.violation_count = metric.violation_count+1
                    else:
                        metric.violation = False
                    db.session.commit()
            time.sleep(30)
