import socket
import logging as log
import threading
from http.server import HTTPServer

from flask import Flask
from prometheus_client import Summary, MetricsHandler

app = Flask("prom-gunicorn-ex")


# Create a metric to track time spent and requests made.
REQUEST_TIME = Summary("request_processing_seconds", "Time spent processing request")

PROMETHEUS_PORT = 9011

# Taken from
# https://github.com/korfuri/django-prometheus/blob/47374565b6ffd8ab066786948305292e8d4df75f/django_prometheus/exports.py#L44-L51
class PrometheusEndpointServer(threading.Thread):
    """A thread class that holds an http and makes it serve_forever()."""
    def __init__(self, httpd, *args, **kwargs):
        self.httpd = httpd
        super(PrometheusEndpointServer, self).__init__(*args, **kwargs)

    def run(self):
        self.httpd.serve_forever()

def start_prometheus_server():
    try:
        httpd = HTTPServer(("0.0.0.0", PROMETHEUS_PORT), MetricsHandler)
    except (OSError, socket.error):
        return

    thread = PrometheusEndpointServer(httpd)
    thread.daemon = True
    thread.start()
    log.info("Exporting Prometheus /metrics/ on port %s", PROMETHEUS_PORT)

start_prometheus_server()

@app.route("/")
@REQUEST_TIME.time()
def hello():
    return "Hello World!"

if __name__ == "__main__":
    app.run()
