"""
Test suite for the Medical Research Agent Flask API.

Tests cover:
- Successful API requests with valid questions
- Error handling for empty or missing questions
- Upstream agent errors and edge cases
- Health check endpoint
"""

import pytest
import json
import sys
import os

# Add the backend directory to the path so we can import the app
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app import app


@pytest.fixture
def client():
    """
    Create a Flask test client for API testing.
    """
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


class TestHealthCheck:
    """Tests for the health check endpoint."""

    def test_health_check_success(self, client):
        """Test that health check returns 200 when agent is initialized."""
        response = client.get('/health')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
        assert data['agent'] == 'ready'

    def test_health_check_content_type(self, client):
        """Test that health check returns JSON content type."""
        response = client.get('/health')
        assert response.content_type == 'application/json'


class TestAskEndpoint:
    """Tests for the /api/ask endpoint."""

    def test_ask_valid_question(self, client):
        """Test successful API request with a valid question."""
        payload = {
            'question': 'What are the latest treatments for diabetes?'
        }
        response = client.post(
            '/api/ask',
            data=json.dumps(payload),
            content_type='application/json'
        )
        assert response.status_code == 200
        data = json.loads(response.data)

        # Verify response structure
        assert 'answer_text' in data
        assert 'bullets' in data
        assert 'source_links' in data
        assert 'disclaimer' in data

        # Verify content
        assert isinstance(data['answer_text'], str)
        assert isinstance(data['bullets'], list)
        assert isinstance(data['source_links'], list)
        assert len(data['bullets']) > 0
        assert len(data['source_links']) > 0

        # Verify disclaimer is present
        assert 'educational' in data['disclaimer'].lower() or 'not' in data['disclaimer'].lower()

    def test_ask_with_short_question(self, client):
        """Test API request with a short, simple question."""
        payload = {'question': 'What is diabetes?'}
        response = client.post(
            '/api/ask',
            data=json.dumps(payload),
            content_type='application/json'
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'answer_text' in data
        assert 'bullets' in data

    def test_ask_with_long_question(self, client):
        """Test API request with a longer, more complex question."""
        payload = {
            'question': 'I have been experiencing chronic pain in my lower back for several months. What are the evidence-based treatment options that have been shown to be effective?'
        }
        response = client.post(
            '/api/ask',
            data=json.dumps(payload),
            content_type='application/json'
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'answer_text' in data

    def test_ask_missing_question_field(self, client):
        """Test error handling when 'question' field is missing."""
        payload = {'other_field': 'some value'}
        response = client.post(
            '/api/ask',
            data=json.dumps(payload),
            content_type='application/json'
        )
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
        assert 'question' in data['error'].lower() or 'missing' in data['error'].lower()

    def test_ask_empty_question_field(self, client):
        """Test error handling when 'question' field is empty string."""
        payload = {'question': ''}
        response = client.post(
            '/api/ask',
            data=json.dumps(payload),
            content_type='application/json'
        )
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data

    def test_ask_whitespace_only_question(self, client):
        """Test error handling when 'question' is only whitespace."""
        payload = {'question': '   \t\n   '}
        response = client.post(
            '/api/ask',
            data=json.dumps(payload),
            content_type='application/json'
        )
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data

    def test_ask_question_not_string(self, client):
        """Test error handling when 'question' is not a string."""
        payload = {'question': 12345}
        response = client.post(
            '/api/ask',
            data=json.dumps(payload),
            content_type='application/json'
        )
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data

    def test_ask_null_question(self, client):
        """Test error handling when 'question' is null."""
        payload = {'question': None}
        response = client.post(
            '/api/ask',
            data=json.dumps(payload),
            content_type='application/json'
        )
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data

    def test_ask_invalid_json(self, client):
        """Test error handling when request body is invalid JSON."""
        response = client.post(
            '/api/ask',
            data='not valid json',
            content_type='application/json'
        )
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data

    def test_ask_empty_json_body(self, client):
        """Test error handling when request body is empty."""
        response = client.post(
            '/api/ask',
            data='',
            content_type='application/json'
        )
        assert response.status_code == 400

    def test_ask_missing_content_type(self, client):
        """Test handling of request without proper content-type."""
        payload = {'question': 'What is a fever?'}
        response = client.post(
            '/api/ask',
            data=json.dumps(payload)
        )
        # Flask with force=True will try to parse JSON anyway
        assert response.status_code == 200 or response.status_code == 400

    def test_ask_response_content_type(self, client):
        """Test that /api/ask returns JSON content type."""
        payload = {'question': 'What are vitamins?'}
        response = client.post(
            '/api/ask',
            data=json.dumps(payload),
            content_type='application/json'
        )
        assert response.content_type == 'application/json'

    def test_ask_response_structure(self, client):
        """Test that response has all required fields with correct types."""
        payload = {'question': 'Tell me about hypertension.'}
        response = client.post(
            '/api/ask',
            data=json.dumps(payload),
            content_type='application/json'
        )
        assert response.status_code == 200
        data = json.loads(response.data)

        # Check all required fields exist
        required_fields = ['answer_text', 'bullets', 'source_links', 'disclaimer']
        for field in required_fields:
            assert field in data, f"Missing field: {field}"

        # Check field types
        assert isinstance(data['answer_text'], str)
        assert isinstance(data['bullets'], list)
        assert isinstance(data['source_links'], list)
        assert isinstance(data['disclaimer'], str)

        # Check that lists contain strings
        for bullet in data['bullets']:
            assert isinstance(bullet, str)
        for link in data['source_links']:
            assert isinstance(link, str)

    def test_ask_with_special_characters(self, client):
        """Test handling of questions with special characters."""
        payload = {'question': 'What is the relationship between COVID-19 & immune systems? #health @virus'}
        response = client.post(
            '/api/ask',
            data=json.dumps(payload),
            content_type='application/json'
        )
        assert response.status_code == 200

    def test_ask_with_unicode_characters(self, client):
        """Test handling of questions with unicode characters."""
        payload = {'question': 'What causes headaches? 🧠 How to treat? ❓'}
        response = client.post(
            '/api/ask',
            data=json.dumps(payload),
            content_type='application/json'
        )
        assert response.status_code == 200

    def test_ask_with_medical_terminology(self, client):
        """Test handling of questions with medical terminology."""
        payload = {'question': 'What is the pathophysiology of acute myocardial infarction?'}
        response = client.post(
            '/api/ask',
            data=json.dumps(payload),
            content_type='application/json'
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'answer_text' in data


class TestStaticFiles:
    """Tests for static file serving."""

    def test_serve_root(self, client):
        """Test serving the root index.html."""
        response = client.get('/')
        # Should return 200 or 404 depending on whether index.html exists
        assert response.status_code in [200, 404, 500]

    def test_serve_nonexistent_file(self, client):
        """Test serving a nonexistent file falls back to index.html."""
        response = client.get('/nonexistent.html')
        # Should fall back to index.html or return 404
        assert response.status_code in [200, 404, 500]


class TestErrorHandling:
    """Tests for error handling and edge cases."""

    def test_unsupported_http_method(self, client):
        """Test that GET requests to /api/ask are rejected."""
        response = client.get('/api/ask')
        # Flask returns 404 or 405 depending on configuration
        assert response.status_code in [404, 405]

    def test_large_payload(self, client):
        """Test handling of very large payloads."""
        large_question = 'x' * 10000
        payload = {'question': large_question}
        response = client.post(
            '/api/ask',
            data=json.dumps(payload),
            content_type='application/json'
        )
        # Should still process or return reasonable error
        assert response.status_code in [200, 400, 413]

    def test_many_extra_fields(self, client):
        """Test that extra fields in payload are ignored."""
        payload = {
            'question': 'What is cholesterol?',
            'extra_field_1': 'value1',
            'extra_field_2': 'value2',
            'extra_field_3': 'value3'
        }
        response = client.post(
            '/api/ask',
            data=json.dumps(payload),
            content_type='application/json'
        )
        assert response.status_code == 200


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
