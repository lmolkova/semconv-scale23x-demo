# Events: `storage`

This document describes the `storage` events.

## `` ![Development](https://img.shields.io/badge/-development-blue)

Exception occurred during storage client operation.

**Name**: `storage.client.operation.exception`

### Attributes

| Attribute              | Type     | Requirement Level | Description                                                                                                                                                                         |
| ---------------------- | -------- | ----------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `exception.message`    | `string` | Required          | The exception message.                                                                                                                                                              |
| `exception.type`       | `string` | Required          | The type of the exception (its fully-qualified class name, if applicable). The dynamic type of the exception should be preferred over the static type in languages that support it. |
| `exception.stacktrace` | `string` | Recommended       | A stacktrace as a string in the natural representation for the language runtime. The representation is to be determined and documented by each language SIG.                        |
