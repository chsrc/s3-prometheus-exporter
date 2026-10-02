# S3 Prometheus Exporter

A lightweight Prometheus exporter for S3-compatible object storage.

The exporter periodically scans all accessible S3 buckets and exposes metrics for bucket size, object count, and the most recently modified object. It is designed to work with both AWS S3 and S3-compatible storage such as Ceph RGW.

## Metrics

The exporter exposes the following S3 metrics:

| Metric                                               | Description                                                        |
| ---------------------------------------------------- | ------------------------------------------------------------------ |
| `s3_bucket_size_bytes`                               | Total size of objects in each bucket                               |
| `s3_bucket_object_count`                             | Number of objects in each bucket                                   |
| `s3_bucket_last_modified_timestamp_seconds`          | Unix timestamp of the most recently modified object in each bucket |
| `s3_exporter_buckets_total`                          | Number of buckets discovered                                       |
| `s3_exporter_last_successful_scan_timestamp_seconds` | Unix timestamp of the last successful S3 scan                      |

The exporter also exposes the standard Python and process metrics provided by `prometheus-client`.

## Configuration

Configuration is provided through environment variables:

| Variable                   | Default | Description                                   |
| -------------------------- | ------- | --------------------------------------------- |
| `SCAN_INTERVAL_SECONDS`    | `900`   | Time between S3 scans                         |
| `METRICS_PORT`             | `9222`  | HTTP port for `/metrics`                      |
| `AWS_REGION`               | —       | S3 region                                     |
| `AWS_ENDPOINT`             | —       | S3-compatible endpoint                        |
| `AWS_SIGNATURE_VERSION`    | `v4`    | S3 signature version                          |
| `AWS_S3_FORCE_PATH_STYLE`  | `false` | Use path-style S3 addressing                  |
| `AWS_INSECURE_SKIP_VERIFY` | `false` | Disable TLS certificate verification          |
| `FAKE_S3`                  | `false` | Debug: Use fake S3 data instead of a real S3 service |

AWS credentials are read from the standard environment variables:

```text
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
```

### Example

```bash
export AWS_ENDPOINT="https://s3.example.com"
export AWS_REGION="us-east-1"
export AWS_ACCESS_KEY_ID="..."
export AWS_SECRET_ACCESS_KEY="..."
export AWS_S3_FORCE_PATH_STYLE="true"

s3-prometheus-exporter
```

## Running locally

Install the package:

```bash
pip install .
```

Run the exporter:

```bash
s3-prometheus-exporter
```

The metrics endpoint will then be available at:

```text
http://localhost:9222/metrics
```

For development without an S3 service, enable the fake client:

```bash
FAKE_S3=true s3-prometheus-exporter
```

## Docker

The exporter is published as a container image:

```text
ghcr.io/chsrc/s3-prometheus-exporter
```

Run it with:

```bash
docker run --rm \
  -p 9222:9222 \
  -e AWS_ENDPOINT="https://s3.example.com" \
  -e AWS_REGION="us-east-1" \
  -e AWS_ACCESS_KEY_ID="..." \
  -e AWS_SECRET_ACCESS_KEY="..." \
  ghcr.io/chsrc/s3-prometheus-exporter:main
```

## Kubernetes

A Helm chart is provided in:

```text
helm/s3-prometheus-exporter
```

The exporter is deployed to Kubernetes and exposes port `9222` for Prometheus scraping.

To access the metrics endpoint locally:

```bash
kubectl -n s3-metrics port-forward svc/s3-exporter <local-port>:9222
```

Then open:

```text
http://localhost:<local-port>/metrics
```

## Prometheus

The exporter can be scraped using a standard Prometheus scrape configuration, e.g.:

```yaml
- job_name: s3-exporter
  scrape_interval: 15m
  static_configs:
    - targets:
        - s3-exporter.s3-metrics.svc.cluster.local:9222
```

The exporter scan interval and Prometheus scrape interval are independent. The default is 15 minutes.

## Development

Run the test suite with:

```bash
pytest
```

The project uses Python 3.12.

## License

See the repository for licensing information.
