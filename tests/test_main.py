from unittest.mock import Mock

import main


def test_check_url(monkeypatch):
    mock_response = Mock()
    mock_response.status_code = 200

    monkeypatch.setattr(main.httpx, "get", lambda url, timeout: mock_response)

    result = main.check_url("https://example.com")

    assert result["url"] == "https://example.com"
    assert result["status"] == 200


def test_check_url_returns_unhealthy_status(monkeypatch):
    mock_response = Mock()
    mock_response.status_code = 503

    monkeypatch.setattr(main.httpx, "get", lambda url, timeout: mock_response)

    result = main.check_url("http://broken.example.com")

    assert result["status"] == 503


def test_check_url_classifies_2xx_as_healthy(monkeypatch):
    mock_response = Mock(status_code=204)
    monkeypatch.setattr(main.httpx, "get", lambda url, timeout: mock_response)

    result = main.check_url("https://example.com/health")

    assert result["healthy"] is True


def test_check_url_classifies_non_2xx_as_unhealthy(monkeypatch):
    mock_response = Mock(status_code=301)
    monkeypatch.setattr(main.httpx, "get", lambda url, timeout: mock_response)

    result = main.check_url("https://example.com/health")

    assert result["healthy"] is False


def test_check_url_handles_network_errors(monkeypatch):
    def fail(url, timeout):
        raise main.httpx.ConnectError("connection failed")

    monkeypatch.setattr(main.httpx, "get", fail)

    result = main.check_url("https://example.com")

    assert result["healthy"] is False
    assert result["status"] is None
    assert result["error"] == "connection failed"


def test_check_url_handles_timeouts(monkeypatch):
    def fail(url, timeout):
        raise main.httpx.ReadTimeout("request timed out")

    monkeypatch.setattr(main.httpx, "get", fail)

    result = main.check_url("https://example.com")

    assert result["healthy"] is False
    assert result["status"] is None
    assert result["error"] == "request timed out"


def test_check_url_uses_request_timeout(monkeypatch):
    observed = {}

    def get(url, timeout):
        observed["timeout"] = timeout
        return Mock(status_code=200)

    monkeypatch.setattr(main.httpx, "get", get)

    main.check_url("https://example.com")

    assert observed["timeout"] == main.REQUEST_TIMEOUT_SECONDS


def test_main_rejects_wrong_number_of_arguments(capsys):
    assert main.main(["main.py"]) == 2
    assert "usage: main.py URL" in capsys.readouterr().err

    assert main.main(["main.py", "https://example.com", "extra"]) == 2
    assert "usage: main.py URL" in capsys.readouterr().err


def test_main_rejects_non_http_url(capsys):
    exit_code = main.main(["main.py", "ftp://example.com"])

    assert exit_code == 2
    assert "must use http:// or https://" in capsys.readouterr().err


def test_main_rejects_url_without_hostname(capsys):
    exit_code = main.main(["main.py", "https:///health"])

    assert exit_code == 2
    assert "missing a hostname" in capsys.readouterr().err


def test_main_returns_nonzero_for_unhealthy_response(monkeypatch):
    monkeypatch.setattr(
        main,
        "check_url",
        lambda url: {
            "url": url,
            "status": 503,
            "response_time": 0.01,
            "healthy": False,
            "error": None,
        },
    )

    assert main.main(["main.py", "https://example.com"]) == 1


def test_main_returns_zero_for_healthy_response(monkeypatch):
    monkeypatch.setattr(
        main,
        "check_url",
        lambda url: {
            "url": url,
            "status": 200,
            "response_time": 0.01,
            "healthy": True,
            "error": None,
        },
    )

    assert main.main(["main.py", "https://example.com"]) == 0
