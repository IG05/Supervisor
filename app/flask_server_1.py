#flask_Server_1
from flask import Flask, request
from prometheus_flask_exporter import PrometheusMetrics
from kafka import KafkaProducer
import json
import logging
import os

app = Flask(__name__)
metrics = PrometheusMetrics(app)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'kafka:9092')


# Kafka producer setup
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,  # use container hostname kafka, or localhost if running locally
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
    logger.info("About to send message to Kafka")
    producer.send('test_topic', value=data)
    logger.info("Sent message to Kafka, about to flush")
    producer.flush()
    logger.info(f"Produced message: {data}")
    return f"Message sent to Kafka: {data}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6200)
