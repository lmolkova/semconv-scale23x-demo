from contextlib import AbstractContextManager
from typing import Optional
from opentelemetry.trace import Tracer, Span, SpanKind


from .attributes import STORAGE_BUCKET, STORAGE_OPERATION_NAME


def start_storage_client_operation(
    tracer: Tracer,
    name: str,
    server_address: Optional[str] = None,
    server_port: Optional[int] = None,
    storage_bucket: Optional[str] = None,
    storage_operation_name: Optional[str] = None,
) -> AbstractContextManager[Span]:
    """Storage client operation."""
    attrs = {
        "server.address": server_address,
        "server.port": server_port,
        STORAGE_BUCKET: storage_bucket,
        STORAGE_OPERATION_NAME: storage_operation_name,
    }
    return tracer.start_as_current_span(
        name,
        kind=SpanKind.CLIENT,
        attributes={k: v for k, v in attrs.items() if v is not None},
    )
