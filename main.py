import sys
from time import perf_counter
from urllib.parse import urlparse

import httpx

REQUEST_TIMEOUT_SECONDS = 5.0


def check_args(argv: list[str]) -> str:
    if len(argv) != 2:
        raise ValueError("usage: main.py URL")

    return argv[1]


def check_url_is_valid(url: str) -> str:
    try:
        parsed = urlparse(url)
        hostname = parsed.hostname
    except ValueError as exc:
        raise ValueError(f"invalid URL: {exc}") from exc

    if parsed.scheme not in ("http", "https"):
        raise ValueError("URL must use http:// or https://")

    if not hostname:
        raise ValueError("URL is missing a hostname")

    return url


def check_url(url: str) -> dict[str, object]:
    start_time = perf_counter()

    try:
        response = httpx.get(url, timeout=REQUEST_TIMEOUT_SECONDS)
    except httpx.RequestError as exc:
        return {
            "url": url,
            "status": None,
            "response_time": perf_counter() - start_time,
            "healthy": False,
            "error": str(exc),
        }

    elapsed_time = perf_counter() - start_time

    return {
        "url": url,
        "status": response.status_code,
        "response_time": elapsed_time,
        "healthy": 200 <= response.status_code < 300,
        "error": None,
    }


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv if argv is None else argv

    try:
        user_url = check_url_is_valid(check_args(argv))
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2

    result = check_url(user_url)

    print("URL:", result["url"])
    if result["status"] is not None:
        print("Status:", result["status"])
    else:
        print("Error:", result["error"], file=sys.stderr)
    print(f"Response time: {result['response_time']:.3f} seconds")
    print("Health:", "healthy" if result["healthy"] else "unhealthy")

    return 0 if result["healthy"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
