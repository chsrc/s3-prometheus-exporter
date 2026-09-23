from prometheus_client import Gauge


bucket_size_bytes = Gauge(
    "s3_bucket_size_bytes",
    "Total size of objects in an S3 bucket in bytes.",
    ["bucket"],
)

bucket_object_count = Gauge(
    "s3_bucket_object_count",
    "Number of objects in an S3 bucket.",
    ["bucket"],
)

buckets_total = Gauge(
    "s3_exporter_buckets_total",
    "Number of S3 buckets discovered.",
)

last_successful_scan = Gauge(
    "s3_exporter_last_successful_scan_timestamp_seconds",
    "Unix timestamp of the last successful S3 scan.",
)

last_modified_timestamp = Gauge(
    "s3_bucket_last_modified_timestamp_seconds",
    "Unix timestamp of the most recently modified object in an S3 bucket.",
    ["bucket"],
)

def update_metrics(stats):
    buckets_total.set(len(stats))

    for bucket in stats:
        bucket_size_bytes.labels(
            bucket=bucket.name
        ).set(bucket.size_bytes)

        bucket_object_count.labels(
            bucket=bucket.name
        ).set(bucket.object_count)

        if bucket.last_modified_timestamp is not None:
            last_modified_timestamp.labels(
                bucket=bucket.name
            ).set(bucket.last_modified_timestamp)
