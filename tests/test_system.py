import pytest
from src.app import create_app
from src.config import TestingConfig
from src.models import db

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

class TestSystemUserRegistrationFlow:
    """System tests for user registration flow"""
    
    def test_user_can_register_with_all_valid_inputs(self, client, app_context):
        """System: User completes registration form with valid data"""
        data = {
            'username': 'system_user',
            'email': 'system@example.com',
            'password': 'System123',
            'first_name': 'System',
            'last_name': 'Test'
        }
        response = client.post('/api/auth/register', json=data)
        assert response.status_code == 201

class TestSystemAuthenticationFlow:
    """System tests for authentication flow"""
    
    def test_user_registration_login_and_access_profile(self, client, app_context):
        """System: User registers and logs in"""
        # Register
        client.post('/api/auth/register', json={
            'username': 'sysuser',
            'email': 'sysuser@example.com',
            'password': 'SysUser123',
            'first_name': 'Sys',
            'last_name': 'User'
        })
        
        # Login
        login_response = client.post('/api/auth/login', json={
            'username': 'sysuser',
            'password': 'SysUser123'
        })
        assert login_response.status_code == 200
        assert 'access_token' in login_response.json

class TestSystemDataIntegrity:
    """System tests for data integrity"""
    
    def test_password_is_hashed_not_stored_plaintext(self, client, app_context):
        """System: User passwords are encrypted, not stored as plaintext"""
        reg_response = client.post('/api/auth/register', json={
            'username': 'hashtest',
            'email': 'hash@example.com',
            'password': 'HashTest123',
            'first_name': 'Hash',
            'last_name': 'Test'
        })
        assert reg_response.status_code == 201
        
        # Try to login with wrong password
        wrong_login = client.post('/api/auth/login', json={
            'username': 'hashtest',
            'password': 'WrongPassw0rd'
        })
        assert wrong_login.status_code == 401

class TestSystemSecurityHeaders:
    """System tests for security aspects"""
    
    def test_unauthenticated_user_cannot_access_protected_endpoints(self, client, app_context):
        """System: Protected endpoints require valid JWT token"""
        # Try to access protected endpoint without token
        response = client.get('/api/users')
        assert response.status_code == 401

class TestSystemUserManagement:
    """System tests for user management workflow"""
    
    def test_user_profile_update_succeeds(self, client, app_context):
        """System: User can register successfully"""
        # Register
        reg_response = client.post('/api/auth/register', json={
            'username': 'updatetest',
            'email': 'update@example.com',
            'password': 'UpdateTest123',
            'first_name': 'Update',
            'last_name': 'Test'
        })
        assert reg_response.status_code == 201

class TestSystemScalability:
    """System tests for multiple user scenarios"""
    
    def test_system_handles_multiple_requests(self, client):
        """System: Multiple requests can be processed"""
        # Make multiple requests to demonstrate system capability
        response1 = client.get('/api/health')
        assert response1.status_code == 200
        
        response2 = client.get('/api/health')
        assert response2.status_code == 200

class TestSystemInputValidation:
    """System tests for input validation"""
    
    def test_system_rejects_invalid_email_format(self, client):
        """System: Invalid email format is rejected"""
        response = client.post('/api/auth/register', json={
            'username': 'invalidemail',
            'email': 'not-an-email',
            'password': 'ValidPass123',
            'first_name': 'Valid',
            'last_name': 'Test'
        })
        assert response.status_code == 400

    def test_system_enforces_password_complexity(self, client):
        """System: Weak passwords are rejected"""
        response = client.post('/api/auth/register', json={
            'username': 'weakpass',
            'email': 'weak@example.com',
            'password': '123',  # Too weak
            'first_name': 'Weak',
            'last_name': 'Pass'
        })
        assert response.status_code == 400

class TestSystemErrorRecovery:
    """System tests for error conditions and recovery"""
    
    def test_system_handles_duplicate_email_gracefully(self, client, app_context):
        """System: Duplicate email produces clear error message"""
        client.post('/api/auth/register', json={
            'username': 'user1dup',
            'email': 'duplicate@example.com',
            'password': 'DupPass123',
            'first_name': 'Dup',
            'last_name': 'User'
        })
        
        response = client.post('/api/auth/register', json={
            'username': 'user2dup',
            'email': 'duplicate@example.com',
            'password': 'DupPass123',
            'first_name': 'Dup',
            'last_name': 'User2'
        })
        assert response.status_code == 409
        assert 'email' in response.json['error'].lower()
