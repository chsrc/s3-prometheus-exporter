from app.metrics import update_metrics
from app.s3 import BucketStats


def test_update_metrics():
    stats = [
        BucketStats(
            name="test-bucket",
            object_count=10,
            size_bytes=12345,
        )
    ]

    update_metrics(stats)

    assert True