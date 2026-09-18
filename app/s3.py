from dataclasses import dataclass

import boto3
from botocore.config import Config


@dataclass
class BucketStats:
    name: str
    object_count: int
    size_bytes: int


class S3Client:
    def __init__(
        self,
        region_name: str | None = None,
        endpoint_url: str | None = None,
        signature_version: str = "v4",
        force_path_style: bool = False,
        insecure_skip_verify: bool = False,
    ):
        addressing_style = (
            "path" if force_path_style else "auto"
        )

        config = Config(
            signature_version=signature_version,
            s3={
                "addressing_style": addressing_style,
            },
        )

        self.client = boto3.client(
            "s3",
            region_name=region_name,
            endpoint_url=endpoint_url,
            verify=not insecure_skip_verify,
            config=config,
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

        paginator = self.client.get_paginator(
            "list_objects_v2"
        )

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


class FakeS3Client:
    def collect(self) -> list[BucketStats]:
        return [
            BucketStats(
                name="example-data",
                object_count=1234,
                size_bytes=1024 * 1024 * 512,
            ),
            BucketStats(
                name="example-backups",
                object_count=5678,
                size_bytes=1024 * 1024 * 1024 * 12,
            ),
        ]