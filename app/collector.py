import logging
import time

from .metrics import last_successful_scan, update_metrics
from .s3 import S3Client

logger = logging.getLogger(__name__)


class Collector:
    def __init__(self, s3: S3Client):
        self.s3 = s3

    def collect(self) -> None:
        logger.info("Starting S3 scan")

        start = time.monotonic()

        try:
            stats = self.s3.collect()
            update_metrics(stats)

            last_successful_scan.set(time.time())

            duration = time.monotonic() - start

            logger.info(
                "S3 scan completed: buckets=%d duration=%.2fs",
                len(stats),
                duration,
            )

        except Exception:
            logger.exception("S3 scan failed")

    def run_forever(self, interval_seconds: int) -> None:
        while True:
            self.collect()
            time.sleep(interval_seconds)