from dataclasses import dataclass

import boto3


@dataclass
class BucketStats:
    name: str
    object_count: int
    size_bytes: int


class S3Client:
    def __init__(self, region_name: str | None = None):
        self.client = boto3.client(
            "s3",
            region_name=region_name,
        )

    def list_buckets(self) -> list[str]:
        response = self.client.list_buckets()

        return [
            bucket["Name"]
            for bucket in response.get("Buckets", [])
        ]

    def get_bucket_stats(self, bucket: str) -> BucketStats:
        object_count = 0
        size_bytes = 0

        paginator = self.client.get_paginator("list_objects_v2")

        for page in paginator.paginate(Bucket=bucket):
            for obj in page.get("Contents", []):
                object_count += 1
                size_bytes += obj.get("Size", 0)

        return BucketStats(
            name=bucket,
            object_count=object_count,
            size_bytes=size_bytes,
        )

    def collect(self) -> list[BucketStats]:
        return [
            self.get_bucket_stats(bucket)
            for bucket in self.list_buckets()
        ]