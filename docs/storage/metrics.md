# Metrics: `storage`

This document describes the `storage` metrics.

## `storage.client.operation.active` ![Development](https://img.shields.io/badge/-development-blue)

Number of active storage client operations.

**Instrument**: `updowncounter`

**Unit**: `{operation}`

### Attributes

| Attribute                | Type     | Requirement Level | Description                        |
| ------------------------ | -------- | ----------------- | ---------------------------------- |
| `server.address`         | `string` | Required          | Name of the database host.         |
| `server.port`            | `int`    | Required          | Server port number.                |
| `storage.bucket`         | `string` | Required          | The name of the storage bucket     |
| `storage.operation.name` | Enum     | Required          | The name of the storage operation. |

## `storage.client.operation.duration` ![Development](https://img.shields.io/badge/-development-blue)

Duration of storage client operation.

**Instrument**: `histogram`

**Unit**: `s`

### Attributes

| Attribute                | Type     | Requirement Level                                            | Description                        |
| ------------------------ | -------- | ------------------------------------------------------------ | ---------------------------------- |
| `server.address`         | `string` | Required                                                     | Name of the database host.         |
| `server.port`            | `int`    | Required                                                     | Server port number.                |
| `storage.bucket`         | `string` | Required                                                     | The name of the storage bucket     |
| `storage.operation.name` | Enum     | Required                                                     | The name of the storage operation. |
| `error.type`             | Enum     | Conditionally Required - if and only if operation has failed | The full name of exception type.   |
