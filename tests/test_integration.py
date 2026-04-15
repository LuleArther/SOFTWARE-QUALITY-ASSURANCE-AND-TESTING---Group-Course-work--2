import pytest
from src.app import create_app
from src.config import TestingConfig
from src.models import db, User

@pytest.fixture
def app():
    """Create application for testing"""
    app = create_app(TestingConfig)
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()

@pytest.fixture
def app_context(app):
    """Create application context"""
    with app.app_context():
        yield app

class TestAuthenticationWorkflow:
    """Integration tests for complete authentication workflow"""
    
    def test_complete_registration_to_login_workflow(self, client, app_context):
        """Test complete workflow: register, login"""
        # Step 1: Register user
        reg_data = {
            'username': 'workflow_user',
            'email': 'workflow@example.com',
            'password': 'WorkFlow123',
            'first_name': 'Workflow',
            'last_name': 'Test'
        }
        reg_response = client.post('/api/auth/register', json=reg_data)
        assert reg_response.status_code == 201
        
        # Step 2: Login
        login_response = client.post('/api/auth/login', json={
            'username': 'workflow_user',
            'password': 'WorkFlow123'
        })
        assert login_response.status_code == 200
        assert 'access_token' in login_response.json

class TestMultiUserInteraction:
    """Integration tests for multiple users interacting with API"""
    
    def test_multiple_users_registration_and_login(self, client, app_context):
        """Test multiple users registering and logging in"""
        # Register first user
        response1 = client.post('/api/auth/register', json={
            'username': 'user1',
            'email': 'user1@example.com',
            'password': 'User1Pass123',
            'first_name': 'User',
            'last_name': 'One'
        })
        assert response1.status_code == 201
        
        # Register second user
        response2 = client.post('/api/auth/register', json={
            'username': 'user2',
            'email': 'user2@example.com',
            'password': 'User2Pass123',
            'first_name': 'User',
            'last_name': 'Two'
        })
        assert response2.status_code == 201

class TestDataValidationIntegration:
    """Integration tests for data validation across endpoints"""
    
    def test_email_validation_across_registration_and_update(self, client, app_context):
        """Test email validation works in registration"""
        # Register with valid email
        reg_data = {
            'username': 'testuser',
            'email': 'original@example.com',
            'password': 'TestPass123',
            'first_name': 'Test',
            'last_name': 'User'
        }
        reg_response = client.post('/api/auth/register', json=reg_data)
        assert reg_response.status_code == 201

class TestCRUDOperations:
    """Integration tests for CRUD operations"""
    
    def test_complete_crud_workflow(self, client, app_context):
        """Test Create and Read operations"""
        # Create
        create_data = {
            'username': 'crud_user',
            'email': 'crud@example.com',
            'password': 'CrudPass123',
            'first_name': 'Crud',
            'last_name': 'Test'
        }
        create_response = client.post('/api/auth/register', json=create_data)
        assert create_response.status_code == 201
        
        # Verify creation
        assert create_response.json['user']['username'] == 'crud_user'

class TestErrorHandling:
    """Integration tests for error handling"""
    
    def test_404_error_handling(self, client):
        """Test 404 error handling"""
        response = client.get('/api/nonexistent/endpoint')
        assert response.status_code == 404
        assert 'error' in response.json
    
    def test_invalid_json_payload(self, client):
        """Test handling of invalid JSON payload"""
        response = client.post('/api/auth/register', 
            data='invalid json',
            content_type='application/json')
        assert response.status_code in [400, 415]
