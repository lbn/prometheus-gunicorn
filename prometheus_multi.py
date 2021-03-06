import threading
from http.server import HTTPServer
import socket
import logging as log
import atexit
# get_ip_address
from sh import ip, awk, cut

import prometheus_client
import consul


# Do not use addr and remove the address option from the register function
# if you are running this on a regular instance with a local Consul agent
addr = cut(awk(ip("addr", "show", "dev", "eth0"), "/inet / { print $2 }"), "-d/", "-f1").strip()
print(addr)

# consul should be a hostname that is accessible from the clever app container
c = consul.Consul(host="consul")

def deregister_id(service_id):
    def dereg():
        c.agent.service.deregister(service_id)
    return dereg

def start_prometheus_server(name, port_range):
    for port in range(*port_range):
        try:
            httpd = HTTPServer(("0.0.0.0", port), prometheus_client.MetricsHandler)
        except (OSError, socket.error):
            # Python 2 raises socket.error, in Python 3 socket.error is an
            # alias for OSError
            continue  # Try next port
        service_id = "{}-{}".format(name, port)
        c.agent.service.register(name, service_id=service_id, address=addr, port=port, tags=["prometheus"])
        atexit.register(deregister_id(service_id))

        thread = PrometheusEndpointServer(httpd)
        thread.daemon = True
        thread.start()
        log.info("Exporting Prometheus /metrics/ on port %s", port)
        return # Stop trying ports at this point


class PrometheusEndpointServer(threading.Thread):
    """A thread class that holds an http and makes it serve_forever()."""
    def __init__(self, httpd, *args, **kwargs):
        self.httpd = httpd
        super(PrometheusEndpointServer, self).__init__(*args, **kwargs)

    def run(self):
        self.httpd.serve_forever()
