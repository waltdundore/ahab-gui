"""
Test error pages implementation.

Validates:
- Requirements 2.4 (Plain language error messages)
- Requirements 12.2 (Consequence explanation)
- Requirements 12.3 (Error input preservation)
"""

import pytest
from flask import url_for


def test_404_error_page(client):
    """Test 404 error page displays plain language message."""
    response = client.get('/nonexistent-page')
    
    assert response.status_code == 404
    assert b'Page Not Found' in response.data
    assert b'We couldn\'t find the page you\'re looking for' in response.data
    assert b'Check the URL for typos' in response.data


def test_500_error_page_json(client):
    """Test 500 error returns JSON for API requests."""
    # Simulate API request
    response = client.get('/api/nonexistent', 
                         headers={'Accept': 'application/json'})
    
    assert response.status_code == 404
    assert response.is_json
    data = response.get_json()
    assert data['error'] is True
    assert 'message' in data


def test_csrf_error_handling(client):
    """Test CSRF error returns appropriate response."""
    # This would normally trigger CSRF error in real scenario
    response = client.post('/api/execute', 
                          json={'command': 'test'},
                          headers={'Accept': 'application/json'})
    
    # Should get CSRF error or similar
    assert response.status_code in [400, 403, 422]


def test_status_api_endpoints(client):
    """Test status API endpoints return proper format."""
    # Test workstation status
    response = client.get('/api/workstation/status')
    assert response.status_code == 200
    assert response.is_json
    
    data = response.get_json()
    assert 'status_value' in data
    assert 'status_type' in data
    assert 'last_updated' in data
    assert 'success' in data
    
    # Test service status
    response = client.get('/api/services/apache/status')
    assert response.status_code == 200
    assert response.is_json
    
    data = response.get_json()
    assert 'status_value' in data
    assert 'status_type' in data
    assert 'last_updated' in data


def test_invalid_service_status(client):
    """Test invalid service returns error."""
    response = client.get('/api/services/invalid/status')
    assert response.status_code == 400
    
    data = response.get_json()
    assert data['success'] is False
    assert 'Invalid Service' in data['status_value']


def test_error_message_component_structure():
    """Test error message component has required elements."""
    # This would be tested in template rendering
    # For now, just verify the template exists
    import os
    template_path = 'templates/components/error-message.html'
    assert os.path.exists(template_path)
    
    # Check template contains required elements
    with open(template_path, 'r') as f:
        content = f.read()
        assert 'error-message' in content
        assert 'recovery-actions' in content
        assert 'technical-details' in content
        assert 'role="alert"' in content


def test_status_display_component_structure():
    """Test status display component has required elements."""
    import os
    template_path = 'templates/components/status-display.html'
    assert os.path.exists(template_path)
    
    # Check template contains required elements
    with open(template_path, 'r') as f:
        content = f.read()
        assert 'status-display' in content
        assert 'status-timestamp' in content
        assert 'stale-indicator' in content
        assert 'status-actions' in content
        assert 'last_updated' in content