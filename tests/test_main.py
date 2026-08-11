from unittest.mock import Mock

import main


def test_check_url(monkeypatch):
    mock_response = Mock()
    mock_response.status_code = 200

    monkeypatch.setattr(main.httpx, "get", lambda url: mock_response)

    result = main.check_url("https://example.com")

    assert result["url"] == "https://example.com"
    assert result["status"] == 200

def test_vhech_url_returns_status(monkeypatch):
    mock_response = Mock()
    mock_response.status_code = 503

    monkeypatch.setattr(main.httpx, "get", lambda url: mock_response)

    result = main.check_url("http://broken.example.com")

    assert result["status"] == 503
