#flask_Server_1
from flask import Flask, request
from prometheus_flask_exporter import PrometheusMetrics
from kafka import KafkaProducer
import json
import logging

app = Flask(__name__)
metrics = PrometheusMetrics(app)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Kafka producer setup
producer = KafkaProducer(
    bootstrap_servers='host.docker.internal:9092',  # use container hostname kafka, or localhost if running locally
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

@app.route('/')
def hello():
    logger.info("Hello route hit")
    return "Flask Server 1 (Producer) is running"

@app.route('/produce')
def produce():
    data = {
        "message": request.args.get('message', 'Hello Kafka!'),
        "id": request.args.get('id', '0')
    }
    producer.send('test_topic', value=data)
    producer.flush()
    logger.info(f"Produced message: {data}")
    return f"Message sent to Kafka: {data}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6200)
