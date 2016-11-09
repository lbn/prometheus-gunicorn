# prometheus-gunicorn
Using Prometheus properly with gunicorn

## Tutorial
Services registered with Consul for clever_app:
```sh
docker run --net prometheusgunicorn_default -it --rm clue/httpie consul:8500/v1/catalog/service/prom-gunicorn-clever
```
Load test with `boom`/`hey`:
```sh
docker run --rm  williamyeh/boom -n 100 -c 10 http://172.17.0.1:9010
```
