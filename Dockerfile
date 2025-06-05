FROM python:3.11-slim

# Install Supervisor and any system dependencies
RUN apt-get update && apt-get install -y supervisor && \
    mkdir -p /var/log/supervisor

# Copy app and install Python packages
WORKDIR /app
COPY app /app
COPY supervisord.conf /etc/supervisord.conf
RUN pip install --no-cache-dir -r requirements.txt

# Expose Flask port
EXPOSE 6200
EXPOSE 6201
# Start Supervisor to run both flask and celery
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisord.conf"]
