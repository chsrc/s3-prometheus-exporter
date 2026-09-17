FROM python:3.12-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

COPY pyproject.toml .
COPY app ./app

RUN pip install --no-cache-dir .

USER nobody

LABEL org.opencontainers.image.source=https://github.com/chsrc/S3-prometheus-exporter

CMD ["s3-prometheus-exporter"]
