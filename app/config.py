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


settings = Settings()