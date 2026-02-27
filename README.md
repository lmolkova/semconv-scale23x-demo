# Semantic Conventions Tooling Demo

Demo for a conference talk on working with [OpenTelemetry Semantic Conventions](https://opentelemetry.io/docs/specs/semconv/) and [Weaver](https://github.com/open-telemetry/weaver) — a toolchain for defining, validating, and generating code from custom semantic conventions.

The demo defines custom storage conventions (`conventions/src`) and uses Weaver to:

- generate Python instrumentation helpers (`conventions_py/`)
- generate Markdown documentation (`docs/`)
- validate naming conventions and backwards compatibility

## Running the demo

Starts the app, S3 mock, OTel Collector, and Grafana LGTM stack:

```sh
docker compose up
```

- App: <http://localhost:8000>
- Grafana: <http://localhost:3000>

The `weaver` service runs a live schema check and emits validation results as OTel logs.

## Code generation

Requires a local [Weaver](https://github.com/open-telemetry/weaver) build at `~/repo/weaver/target/debug/weaver`.

| Target                   | Description                                             |
| ------------------------ | ------------------------------------------------------- |
| `make generate`          | Generate docs and Python helpers                        |
| `make check-conventions` | Validate naming conventions and backwards compatibility |

## TODOs:

- resolition weidness
