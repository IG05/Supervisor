#flask_Server_2
from flask import Flask
from prometheus_flask_exporter import PrometheusMetrics
from kafka import KafkaConsumer
import json
import threading
import logging
from tasks import add  # import celery task

app = Flask(__name__)
metrics = PrometheusMetrics(app)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Kafka consumer setup
consumer = KafkaConsumer(
    'test_topic',
    bootstrap_servers='host.docker.internal:9092',
    auto_offset_reset='earliest',
    group_id='flask_server_2_group',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

def consume_messages():
    for message in consumer:
        data = message.value
        logger.info(f"Consumed message: {data}")
        # Trigger celery task asynchronously with message id and message text (or adapt)
        add.delay(int(data.get('id', 0)), len(data.get('message', '')))
        logger.info("Celery task add() triggered")

# Run Kafka consumer in separate thread
threading.Thread(target=consume_messages, daemon=True).start()

@app.route('/')
def hello():
    return "Flask Server 2 (Consumer) running"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6201)
