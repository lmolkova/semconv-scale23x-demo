import logging
from contextlib import contextmanager
import random
from time import sleep
import timeit
from typing import Optional
from urllib.parse import urlparse
import boto3
from botocore.exceptions import ClientError
from opentelemetry.trace import get_tracer, StatusCode
from opentelemetry.metrics import get_meter
class ConflictError(Exception):
    pass

logger = logging.getLogger(__name__)

tracer = get_tracer(__name__)
meter = get_meter(__name__)
operation_duration = meter.create_histogram("storage.client.operation.duration",
                    unit="s",
                    description="Duration of storage operations",
                    explicit_bucket_boundaries_advisory=[ 0.005, 0.01, 0.025, 0.05, 0.075, 0.1, 0.25, 0.5, 0.75, 1, 2.5, 5, 7.5, 10 ])
class Storage:
    def __init__(self, bucket: str, endpoint_url: Optional[str] = None):
        self.bucket = bucket
        self.common_attributes = {"storage.bucket": bucket}
        if endpoint_url:
            parsed = urlparse(endpoint_url)
            if parsed.hostname:
                self.common_attributes["server.address"] = parsed.hostname
            if parsed.port:
                self.common_attributes["server.port"] = parsed.port
        self._s3 = boto3.client(
            "s3",
            region_name="us-east-1",
            endpoint_url=endpoint_url,
        )

    @contextmanager
    def _traced_operation(self, operation: str, key: str):
        start_time = timeit.default_timer()

        attrs = {**self.common_attributes, "storage.operation.name": operation}
        logger.info(f"{operation}.start", extra={**attrs, "storage.object.key": key})
        with tracer.start_as_current_span(operation, attributes={**attrs, "storage.object.key": key}) as span:
            try:
                yield
            except Exception as e:
                attrs["error.type"] = type(e).__qualname__
                span.set_status(StatusCode.ERROR, str(e))
                logger.warning(f"{operation}.failed", exc_info=e)
                raise
            finally:
                operation_duration.record(timeit.default_timer() - start_time, attributes=attrs)
                logger.info(f"{operation}.end")

    def upload_bytes(self, data: bytes, key: str, content_type: str = "application/octet-stream") -> None:
        with self._traced_operation("upload", key):
            try:
                self._s3.head_object(Bucket=self.bucket, Key=key)
                raise ConflictError(f"Object with key '{key}' already exists in bucket '{self.bucket}'")
            except ClientError:
                pass

            delay = random.uniform(0.1, 0.2)
            sleep(delay)

            chunk_size = 5 * 1024 * 1024
            mpu = self._s3.create_multipart_upload(Bucket=self.bucket, Key=key, ContentType=content_type)
            upload_id = mpu["UploadId"]
            parts = []
            try:
                for i, offset in enumerate(range(0, len(data), chunk_size), start=1):
                    resp = self._s3.upload_part(
                        Bucket=self.bucket, Key=key, UploadId=upload_id,
                        PartNumber=i, Body=data[offset:offset + chunk_size],
                    )
                    parts.append({"PartNumber": i, "ETag": resp["ETag"]})
                self._s3.complete_multipart_upload(
                    Bucket=self.bucket, Key=key, UploadId=upload_id,
                    MultipartUpload={"Parts": parts},
                )
            except Exception:
                self._s3.abort_multipart_upload(Bucket=self.bucket, Key=key, UploadId=upload_id)
                raise

    def download_bytes(self, key: str) -> bytes:
        with self._traced_operation("download", key):
            found = False
            try:
                response = self._s3.get_object(Bucket=self.bucket, Key=key)
                found = True
            except ClientError as e:
                raise e
            if not found:
                sleep(random.uniform(0.05, 0.2))
            return response["Body"].read()
