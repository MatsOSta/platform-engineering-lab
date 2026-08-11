# Repository Instructions

## Project purpose

This repository is a small Python CLI health checker and a platform engineering
portfolio project. The CLI accepts one HTTP or HTTPS URL, performs a timed
request, classifies 2xx responses as healthy, reports failures without exposing
network exception tracebacks, and returns an exit status suitable for scripts
and CI.

The implementation currently lives in `main.py`, with tests in
`tests/test_main.py`. Keep the design appropriate for a small CLI rather than
introducing layers or frameworks without a concrete need.

## Project tooling

- Use `uv` for Python versions, virtual environments, dependency management,
  lockfile maintenance, and command execution.
- Respect `.python-version`, `pyproject.toml`, and `uv.lock`.
- Synchronize locked dependencies with `uv sync --locked` when reproducing CI.
- Add dependencies with the appropriate `uv add` command so both
  `pyproject.toml` and `uv.lock` remain consistent. Prefer the Python standard
  library before adding a dependency, and explain any important dependency
  decision.
- Use `pytest` for tests. Run the full suite with:

  ```text
  uv run python -m pytest
  ```

- Use Ruff for linting and formatting. Before considering work complete, run:

  ```text
  uv run ruff check .
  uv run ruff format --check .
  ```

  Use `uv run ruff format .` when formatting changes are required.

## Engineering expectations

- Keep changes focused on the requested task and do not modify unrelated files.
- Prefer simple, direct implementations over unnecessary abstractions.
- Add type hints where they improve clarity; avoid annotations that add noise
  without making interfaces easier to understand.
- Add or update tests for new behavior and bug fixes.
- Unit tests must be deterministic and must not depend on live external network
  services. Mock HTTP calls or use an in-process transport instead.
- Preserve established CLI behavior unless the requested task intentionally
  changes it, including output streams and exit-code semantics.
- Explain important architecture, behavior, or dependency decisions in the
  final handoff.
- Do not commit or push automatically.

## Completion checks

Before editing, inspect the working tree and relevant files. Preserve existing
user changes. If the test suite already fails before the requested change,
report the failure rather than silently rewriting tests or changing unrelated
behavior to make them pass.

Before considering an implementation complete:

1. Run the full pytest suite.
2. Run Ruff linting.
3. Run the Ruff formatting check.
4. Report the results, along with any check that could not be run.
