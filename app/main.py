from flask import request
from __init__ import make_flask_app
from tasks import add
import logging
from prometheus_flask_exporter import PrometheusMetrics
from prometheus_client import Counter


app = make_flask_app()
metrics = PrometheusMetrics(app)


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

celery_tasks_submitted = Counter('celery_tasks_submitted_total', 'Total Celery tasks submitted')


@app.route('/')
def hello():
    logger.info("Hello route hit")
    return "Flask server is running"

@app.route('/add')
def call_add():
    x = int(request.args.get('x', 1))
    y = int(request.args.get('y', 2))
    result = add.delay(x, y)
    celery_tasks_submitted.inc()  # increment counter when task is submitted
    logger.info(f"Submitted task: add({x}, {y})")
    return f"Task submitted: add({x}, {y})"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6200)  # expose port 6200 to match Docker EXPOSE
