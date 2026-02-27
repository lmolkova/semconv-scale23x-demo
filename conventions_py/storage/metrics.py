from typing import Final, Optional
from opentelemetry.metrics import Meter
from .attributes import STORAGE_BUCKET, STORAGE_OPERATION_NAME

STORAGE_CLIENT_OPERATION_ACTIVE: Final = "storage.client.operation.active"
"""
Number of active storage client operations.
Instrument: updowncounter
Unit: {operation}
"""


class StorageClientOperationActive:
    """
    Number of active storage client operations.
    Instrument: updowncounter
    Unit: {operation}
    """

    def __init__(self, meter: Meter) -> None:
        self._instrument = meter.create_up_down_counter(
            name=STORAGE_CLIENT_OPERATION_ACTIVE,
            description="Number of active storage client operations.",
            unit="{operation}",
        )

    def add(
        self,
        amount: int,
        server_address: str,
        server_port: int,
        storage_bucket: str,
        storage_operation_name: str,
    ) -> None:
        """Number of active storage client operations."""
        attrs = {
            "server.address": server_address,
            "server.port": server_port,
            STORAGE_BUCKET: storage_bucket,
            STORAGE_OPERATION_NAME: storage_operation_name,
        }
        self._instrument.add(
            amount, attributes={k: v for k, v in attrs.items() if v is not None}
        )


STORAGE_CLIENT_OPERATION_DURATION: Final = "storage.client.operation.duration"
"""
Duration of storage client operation.
Instrument: histogram
Unit: s
"""


class StorageClientOperationDuration:
    """
    Duration of storage client operation.
    Instrument: histogram
    Unit: s
    """

    def __init__(self, meter: Meter) -> None:
        self._instrument = meter.create_histogram(
            name=STORAGE_CLIENT_OPERATION_DURATION,
            description="Duration of storage client operation.",
            unit="s",
        )

    def record(
        self,
        amount: float,
        server_address: str,
        server_port: int,
        storage_bucket: str,
        storage_operation_name: str,
        error_type: Optional[str] = None,
    ) -> None:
        """Duration of storage client operation."""
        attrs = {
            "error.type": error_type,
            "server.address": server_address,
            "server.port": server_port,
            STORAGE_BUCKET: storage_bucket,
            STORAGE_OPERATION_NAME: storage_operation_name,
        }
        self._instrument.record(
            amount, attributes={k: v for k, v in attrs.items() if v is not None}
        )
