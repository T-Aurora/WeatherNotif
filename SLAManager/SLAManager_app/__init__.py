import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from PrometheusRetrieval import PrometheusRetriever
import pymysql
import threading
from ViolationCheck import ViolationChecker
pymysql.install_as_MySQLdb()
def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@'+os.getenv('MYSQLHOST','localhost:5509')+'/sla'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db = SQLAlchemy(app)
    class SLAMetric(db.Model):
        __tablename__ = 'sla_metrics'
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(255), nullable=False)
        current_value = db.Column(db.Float)
        desired_value = db.Column(db.Float)
        violation = db.Column(db.Boolean, default=False)
        violation_count = db.Column(db.Integer, default=0)
        # possibile aggiunta di trigger per verificare stato della violation
    with app.app_context():
        db.create_all()
    prom = PrometheusRetriever()
    violation_checker = ViolationChecker()
    violation_thread = threading.Thread(target=violation_checker.check_violations, args=(db,))
    violation_thread.daemon = True
    violation_thread.start()

    @app.route('/sla/metric', methods=['POST'])
    def create_sla_metric():
        name = request.form['name']
        current_value = request.form['current_value'] #usare prom per recuperare valore corrente della metrica
        desired_value = request.form['desired_value']

        new_metric = SLAMetric(name=name, current_value=current_value, desired_value=desired_value)
        db.session.add(new_metric)
        db.session.commit()

        return jsonify({'message': 'SLA metric created successfully'}), 201

    @app.route('/sla/metric/<int:id>', methods=['GET'])
    def get_sla_metric(id):
        metric = SLAMetric.query.get_or_404(id)
        return jsonify({
            'id': metric.id,
            'name': metric.name,
            'current_value': metric.current_value,
            'desired_value': metric.desired_value,
            'violation': metric.violation
        })

    @app.route('/sla/metric/<int:id>', methods=['PUT'])
    def update_sla_metric(id):
        metric = SLAMetric.query.get_or_404(id)
        data = request.json

        metric.name = data.get('name', metric.name)
        metric.desired_value = data.get('desired_value', metric.desired_value)

        db.session.commit()
        return jsonify({'message': 'SLA metric updated successfully'})

    @app.route('/sla/metric/<int:id>', methods=['DELETE'])
    def delete_sla_metric(id):
        metric = SLAMetric.query.get_or_404(id)
        db.session.delete(metric)
        db.session.commit()
        return jsonify({'message': 'SLA metric deleted successfully'})

    @app.route('/sla/metrics', methods=['GET'])
    def get_all_sla_metrics():
        metrics = SLAMetric.query.all()
        result = []
        for metric in metrics:
            metric_data = {
                'id': metric.id,
                'name': metric.name,
                'current_value': metric.current_value,
                'desired_value': metric.desired_value,
                'violation': metric.violation,
                'violation_count': metric.violation_count
            }
            result.append(metric_data)
        return jsonify(result)

    @app.route('/sla/metrics/test', methods=['GET'])
    def test_prometheus():
        query = request.args.get('query')
        res = prom.get_prometheus_metrics_latest_value(query)
        return jsonify(res)
    return app,db