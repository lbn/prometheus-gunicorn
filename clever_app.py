from flask import Flask
from prometheus_client import Summary

from prometheus_multi import start_prometheus_server

app = Flask("prom-gunicorn-clever")

# Create a metric to track time spent and requests made.
REQUEST_TIME = Summary("request_processing_seconds", "Time spent processing request")

start_prometheus_server("prom-gunicorn-clever", port_range=(9011, 9020))

@app.route("/")
@REQUEST_TIME.time()
def hello():
    return "Hello World!"

if __name__ == "__main__":
    app.run()
