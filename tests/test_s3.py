from unittest.mock import MagicMock

from app.s3 import S3Client


def test_get_bucket_stats():
    client = S3Client.__new__(S3Client)

    mock_client = MagicMock()

    mock_client.get_paginator.return_value.paginate.return_value = [
        {
            "Contents": [
                {"Key": "foo.txt", "Size": 100},
                {"Key": "bar.txt", "Size": 200},
            ]
        },
        {
            "Contents": [
                {"Key": "baz.txt", "Size": 300},
            ]
        },
    ]

    client.client = mock_client

    stats = client.get_bucket_stats("test-bucket")

    assert stats.name == "test-bucket"
    assert stats.object_count == 3
    assert stats.size_bytes == 600