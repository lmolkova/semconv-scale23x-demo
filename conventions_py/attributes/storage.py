from typing import Final


from enum import Enum

STORAGE_BUCKET: Final = "storage.bucket"
"""
The name of the storage bucket.
"""

STORAGE_OBJECT_KEY: Final = "storage.object.key"
"""
The key of the object in storage bucket.
"""

STORAGE_OPERATION_NAME: Final = "storage.operation.name"
"""
The name of the storage operation..
"""


class StorageOperationNameValues(Enum):
    UPLOAD = "upload"
    """upload."""
    DOWNLOAD = "download"
    """download."""
