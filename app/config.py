from dataclasses import dataclass
import os


@dataclass(frozen=True)
class Settings:
    scan_interval_seconds: int = int(
        os.getenv("SCAN_INTERVAL_SECONDS", "900")
    )

    metrics_port: int = int(
        os.getenv("METRICS_PORT", "9222")
    )

    aws_region: str | None = os.getenv("AWS_REGION")

    aws_endpoint: str | None = os.getenv("AWS_ENDPOINT")

    aws_signature_version: str = os.getenv(
        "AWS_SIGNATURE_VERSION",
        "v4",
    )

    aws_s3_force_path_style: bool = os.getenv(
        "AWS_S3_FORCE_PATH_STYLE",
        "false",
    ).lower() == "true"

    aws_insecure_skip_verify: bool = os.getenv(
        "AWS_INSECURE_SKIP_VERIFY",
        "false",
    ).lower() == "true"

    fake_s3: bool = os.getenv(
        "FAKE_S3",
        "false",
    ).lower() == "true"


settings = Settings()