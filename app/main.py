import logging

from prometheus_client import start_http_server

from .collector import Collector
from .config import settings
from .s3 import S3Client


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)


def main() -> None:
    start_http_server(settings.metrics_port)

    s3 = S3Client(
        region_name=settings.aws_region,
    )

    collector = Collector(s3)

    collector.run_forever(
        interval_seconds=settings.scan_interval_seconds,
    )


if __name__ == "__main__":
    main()