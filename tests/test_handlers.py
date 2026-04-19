"""
DataPulse Assistant — Unit Tests
Tests for intent detection, input sanitization, file validation, and error handling.
"""
import os
import sys
import pytest

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, allowed_file, sanitize_input


# ─────────────────────────────────────────────
# Test: Input Sanitization
# ─────────────────────────────────────────────

class TestSanitizeInput:
    def test_strips_html_tags(self):
        result = sanitize_input("<script>alert('xss')</script>Hello")
        assert "<script>" not in result
        assert "Hello" in result

    def test_limits_length_to_500_chars(self):
        long_input = "x" * 1000
        result = sanitize_input(long_input)
        assert len(result) == 500

    def test_removes_null_bytes(self):
        result = sanitize_input("hello\x00world")
        assert "\x00" not in result
        assert "helloworld" in result

    def test_strips_whitespace(self):
        result = sanitize_input("   hello world   ")
        assert result == "hello world"

    def test_normal_input_unchanged(self):
        result = sanitize_input("What is the top selling region?")
        assert result == "What is the top selling region?"


# ─────────────────────────────────────────────
# Test: File Extension Validation
# ─────────────────────────────────────────────

class TestFileValidation:
    def test_csv_allowed(self):
        assert allowed_file("data.csv") is True

    def test_xlsx_allowed(self):
        assert allowed_file("report.xlsx") is True

    def test_json_allowed(self):
        assert allowed_file("config.json") is True

    def test_pdf_rejected(self):
        assert allowed_file("document.pdf") is False

    def test_exe_rejected(self):
        assert allowed_file("malware.exe") is False

    def test_no_extension_rejected(self):
        assert allowed_file("noextension") is False

    def test_double_extension_checks_last(self):
        assert allowed_file("data.csv.exe") is False

    def test_uppercase_extension_allowed(self):
        assert allowed_file("DATA.CSV") is True


# ─────────────────────────────────────────────
# Test: Flask Routes (No API keys needed)
# ─────────────────────────────────────────────

class TestFlaskRoutes:
    @pytest.fixture
    def client(self):
        app.config['TESTING'] = True
        with app.test_client() as client:
            yield client

    def test_home_returns_200(self, client):
        response = client.get('/')
        assert response.status_code == 200

    def test_health_endpoint(self, client):
        response = client.get('/health')
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'healthy'

    def test_chat_without_message_returns_400(self, client):
        response = client.post('/chat',
                               json={},
                               content_type='application/json')
        assert response.status_code == 400

    def test_chat_with_empty_message_returns_400(self, client):
        response = client.post('/chat',
                               json={'message': '   '},
                               content_type='application/json')
        assert response.status_code == 400

    def test_upload_no_file_returns_400(self, client):
        response = client.post('/upload-file')
        assert response.status_code == 400

    def test_reset_returns_success(self, client):
        response = client.post('/reset-data')
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True


# ─────────────────────────────────────────────
# Test: Handler Imports (No credentials needed)
# ─────────────────────────────────────────────

class TestHandlerImports:
    def test_gemini_handler_importable(self):
        from assistant.gemini_handler import GeminiHandler
        assert GeminiHandler is not None

    def test_sheets_handler_importable(self):
        from assistant.sheets_handler import SheetsHandler
        assert SheetsHandler is not None

    def test_calendar_handler_importable(self):
        from assistant.calendar_handler import CalendarHandler
        assert CalendarHandler is not None
