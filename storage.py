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
from opentelemetry._logs import get_logger, SeverityNumber
from conventions_py.storage.attributes import (
    STORAGE_BUCKET,
    STORAGE_OBJECT_KEY,
    StorageOperationNameValues,
)
from conventions_py.storage.metrics import StorageClientOperationActive, StorageClientOperationDuration
from conventions_py.storage.spans import start_storage_client_operation
from conventions_py.storage.events import emit_storage_client_operation_exception


class ConflictError(Exception):
    pass


logger = logging.getLogger(__name__)

SCHEMA_URL = "https://localhost:8000/test/me/1.0.0-dev"

tracer = get_tracer(__name__, schema_url=SCHEMA_URL)
meter = get_meter(__name__, schema_url=SCHEMA_URL)
otel_logger = get_logger(__name__, schema_url=SCHEMA_URL)
operation_duration = StorageClientOperationDuration(meter)
active_operations = StorageClientOperationActive(meter)


class Storage:
    def __init__(self, bucket: str, endpoint_url: str):
        self.bucket = bucket
        parsed = urlparse(endpoint_url)
        self._server_address = str(parsed.hostname)  # type: str
        self._server_port = parsed.port or 0 # type: int

        self._s3 = boto3.client(
            "s3",
            region_name="us-east-1",
            endpoint_url=endpoint_url,
        )

    @contextmanager
    def _instrument_operation(self, operation: str, key: str):
        start_time = timeit.default_timer()

        # logger.info(f"{operation}.start", extra={**attrs, STORAGE_OBJECT_KEY: key})
        active_operations.add(
            1,
            server_address=self._server_address,
            server_port=self._server_port,
            storage_bucket=self.bucket,
            storage_operation_name=operation,
        )
        error_type = None
        with start_storage_client_operation(
            tracer,
            f"{operation} {self.bucket}",
            storage_operation_name=operation,
            storage_bucket=self.bucket,
            server_address=self._server_address,
            server_port=self._server_port,
        ) as span:
            if span.is_recording():
                span.set_attribute(STORAGE_OBJECT_KEY, key)
            try:
                yield
            except Exception as e:
                error_type = type(e).__qualname__
                if span.is_recording():
                    span.set_status(StatusCode.ERROR, str(e))
                emit_storage_client_operation_exception(otel_logger, SeverityNumber.WARN, e)
                raise
            finally:
                if error_type:
                    span.set_attribute("error.type", error_type)
                operation_duration.record(
                    timeit.default_timer() - start_time,
                    server_address=self._server_address,
                    server_port=self._server_port,
                    storage_bucket=self.bucket,
                    storage_operation_name=operation,
                    error_type=error_type,
                )
                active_operations.add(
                    -1,
                    server_address=self._server_address,
                    server_port=self._server_port,
                    storage_bucket=self.bucket,
                    storage_operation_name=operation,
                )
                # logger.info(f"{operation}.end")

    def upload_bytes(self, data: bytes, key: str, content_type: str = "application/octet-stream") -> None:
        with self._instrument_operation(StorageOperationNameValues.UPLOAD.value, key):
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
        with self._instrument_operation(StorageOperationNameValues.DOWNLOAD.value, key):
            found = False
            try:
                response = self._s3.get_object(Bucket=self.bucket, Key=key)
                found = True
            except ClientError as e:
                raise e
            if not found:
                sleep(random.uniform(0.05, 0.2))
            return response["Body"].read()
