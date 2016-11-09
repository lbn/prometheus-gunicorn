# prometheus-gunicorn
Using Prometheus properly with gunicorn

## Tutorial
Services registered with Consul for clever_app:
```sh
docker run --net prometheusgunicorn_default -it --rm clue/httpie consul:8500/v1/catalog/service/prom-gunicorn-clever
```
