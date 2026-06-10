"""
Tests para telegram.py y tunnel.py: envio de mensajes y gestion de Cloudflare.
"""
import pytest
import os
import sys
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


class TestSendTelegramMsg:
    @patch("backend.notifier.telegram.requests.post")
    def test_success_returns_true(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response
        from backend.notifier.telegram import send_telegram_msg
        assert send_telegram_msg("token123", "chat456", "Hola") is True

    @patch("backend.notifier.telegram.requests.post")
    def test_failure_returns_false(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_post.return_value = mock_response
        from backend.notifier.telegram import send_telegram_msg
        assert send_telegram_msg("token123", "chat456", "Hola") is False

    @patch("backend.notifier.telegram.requests.post")
    def test_exception_returns_false(self, mock_post):
        mock_post.side_effect = Exception("Network error")
        from backend.notifier.telegram import send_telegram_msg
        assert send_telegram_msg("token123", "chat456", "Hola") is False

    @patch("backend.notifier.telegram.requests.post")
    def test_full_url_and_payload(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response
        from backend.notifier.telegram import send_telegram_msg
        send_telegram_msg("mytoken", "12345", "Test msg")
        mock_post.assert_called_once()
        call_args = mock_post.call_args
        assert "botmytoken" in call_args[0][0]
        assert call_args[1]["json"]["chat_id"] == "12345"
        assert call_args[1]["json"]["text"] == "Test msg"


class TestTunnel:
    def test_dev_mode_true_returns_none(self, monkeypatch):
        monkeypatch.setattr("backend.notifier.tunnel.DEV_MODE", True)
        from backend.notifier.tunnel import get_cf_env_vars
        token, domain = get_cf_env_vars()
        assert token is None
        assert domain is None

    def test_prod_mode_returns_token(self, monkeypatch):
        monkeypatch.setattr("backend.notifier.tunnel.DEV_MODE", False)
        from backend.notifier.tunnel import get_cf_env_vars
        token, domain = get_cf_env_vars()
        assert token is not None
        assert len(token) > 10
        assert domain == "botstake.shop"

    def test_notify_tunnel_url_does_not_crash(self, monkeypatch):
        monkeypatch.setattr("backend.notifier.telegram.send_telegram_msg", lambda *a, **kw: False)
        from backend.notifier.tunnel import notify_tunnel_url
        notify_tunnel_url("https://test.trycloudflare.com")
