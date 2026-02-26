# Spans: `storage`

This document describes the `storage` spans.

## `storage.client.operation` ![Development](https://img.shields.io/badge/-development-blue)

Storage client operation.

**Kind**: `client`

**Name**: `storage.client.operation`

### Attributes

| Attribute                | Type     | Requirement Level                                                                                                  | Description                             |
| ------------------------ | -------- | ------------------------------------------------------------------------------------------------------------------ | --------------------------------------- |
| `error.type`             | Enum     | Conditionally Required - if and only if an error has occurred.                                                     | The full name of exception type.        |
| `server.port`            | `int`    | Conditionally Required - If using a port other than the default port for this DBMS and if `server.address` is set. | Server port number.                     |
| `server.address`         | `string` | Recommended                                                                                                        | Name of the database host.              |
| `storage.bucket`         | `string` | Recommended                                                                                                        | The name of the storage bucket          |
| `storage.object.key`     | `string` | Recommended                                                                                                        | The key of the object in storage bucket |
| `storage.operation.name` | Enum     | Recommended                                                                                                        | The name of the storage operation.      |
