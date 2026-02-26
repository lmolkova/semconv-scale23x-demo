from typing import Final
from opentelemetry.metrics import Meter
from opentelemetry.metrics import Histogram

STORAGE_CLIENT_OPERATION_DURATION: Final = "storage.client.operation.duration"
"""
Duration of storage client operation.
Instrument: histogram
Unit: s
"""


def create_storage_client_operation_duration(meter: Meter) -> Histogram:
    """Duration of storage client operation."""
    return meter.create_histogram(
        name=STORAGE_CLIENT_OPERATION_DURATION,
        description="Duration of storage client operation.",
        unit="s",
    )
