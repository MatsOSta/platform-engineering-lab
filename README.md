# Service Health CLI

A small command-line health checker for HTTP and HTTPS endpoints. It performs a
timed request, treats every `2xx` response as healthy, and returns an exit code
that can be used in scripts and CI pipelines.

Network failures are reported without exposing a Python traceback. Requests
time out after five seconds.

## Run locally

The project requires Python 3.14 or later and uses
[uv](https://docs.astral.sh/uv/) for Python and dependency management.

Install the exact dependencies recorded in `uv.lock`:

```sh
uv sync --locked
```

Check an endpoint:

```sh
uv run python main.py https://example.com
```

Example output:

```text
URL: https://example.com
Status: 200
Response time: 0.123 seconds
Health: healthy
```

The CLI accepts exactly one URL using the `http://` or `https://` scheme.

## Exit codes

| Code | Meaning |
| ---: | --- |
| `0` | The endpoint returned a `2xx` response. |
| `1` | The endpoint returned a non-`2xx` response or the request failed. |
| `2` | The command-line arguments or URL are invalid. |

For example, capture the result in a shell script with:

```sh
uv run python main.py https://example.com
exit_code=$?
```

## Run in a container

Build the image:

```sh
docker build -t service-health .
```

Run the health check:

```sh
docker run --rm service-health https://example.com
```

The container uses the same exit codes as the local command, so its result can
be inspected with `docker inspect` or captured directly by the calling shell.
The runtime image contains only the application and its locked production
dependencies, and runs as a non-root user.

## Development checks

Run the complete test suite:

```sh
uv run python -m pytest
```

Run linting and verify formatting:

```sh
uv run ruff check .
uv run ruff format --check .
```

Tests mock HTTP requests and do not require live network access.

Desired goals:

Developer
    │
    ▼
GitHub
    │
    ├── CI
    │   ├── tests
    │   ├── lint
    │   ├── security scan
    │   ├── SBOM
    │   └── IaC validation/plan
    │
    ▼
Container Registry
    │
    ▼
GitOps
    │
    ▼
AWS
┌─────────────────────────────────┐
│ VPC                             │
│                                 │
│  ┌─────────┐    ┌─────────┐    │
│  │  AZ A   │    │  AZ B   │    │
│  │         │    │         │    │
│  │ EKS     │    │ EKS     │    │
│  │ nodes   │    │ nodes   │    │
│  └─────────┘    └─────────┘    │
│                                 │
│ IAM / Secrets / DNS / Logging   │
└─────────────────────────────────┘
        │
        ▼
Observability
