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

class TestHealth:
    """Unit tests for health check endpoint"""
    
    def test_health_check(self, client):
        """Test health check returns 200"""
        response = client.get('/api/health')
        assert response.status_code == 200
        assert response.json['status'] == 'healthy'
        assert 'timestamp' in response.json

class TestUserRegistration:
    """Unit tests for user registration"""
    
    def test_register_valid_user(self, client, app_context):
        """Test successful user registration"""
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'TestPass123',
            'first_name': 'John',
            'last_name': 'Doe'
        }
        response = client.post('/api/auth/register', json=data)
        assert response.status_code == 201
        assert response.json['user']['username'] == 'testuser'
        assert response.json['user']['email'] == 'test@example.com'
        
        # Verify user in database
        user = User.query.filter_by(username='testuser').first()
        assert user is not None
        assert user.first_name == 'John'
    
    def test_register_no_data(self, client):
        """Test registration with no data"""
        response = client.post('/api/auth/register', json={})
        assert response.status_code == 400
    
    def test_register_missing_field(self, client):
        """Test registration with missing required field"""
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'TestPass123'
        }
        response = client.post('/api/auth/register', json=data)
        assert response.status_code == 400
    
    def test_register_invalid_email(self, client):
        """Test registration with invalid email"""
        data = {
            'username': 'testuser',
            'email': 'invalid-email',
            'password': 'TestPass123',
            'first_name': 'John',
            'last_name': 'Doe'
        }
        response = client.post('/api/auth/register', json=data)
        assert response.status_code == 400
        assert 'email' in response.json['error'].lower()
    
    def test_register_weak_password(self, client):
        """Test registration with weak password"""
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'weak',
            'first_name': 'John',
            'last_name': 'Doe'
        }
        response = client.post('/api/auth/register', json=data)
        assert response.status_code == 400
        assert 'password' in response.json['error'].lower()
    
    def test_register_invalid_username(self, client):
        """Test registration with invalid username"""
        data = {
            'username': 'ab',  # Too short
            'email': 'test@example.com',
            'password': 'TestPass123',
            'first_name': 'John',
            'last_name': 'Doe'
        }
        response = client.post('/api/auth/register', json=data)
        assert response.status_code == 400
        assert 'username' in response.json['error'].lower()
    
    def test_register_duplicate_username(self, client, app_context):
        """Test registration with duplicate username"""
        user_data = {
            'username': 'testuser',
            'email': 'test1@example.com',
            'password': 'TestPass123',
            'first_name': 'John',
            'last_name': 'Doe'
        }
        
        # First registration
        response1 = client.post('/api/auth/register', json=user_data)
        assert response1.status_code == 201
        
        # Second registration with same username
        user_data['email'] = 'test2@example.com'
        response2 = client.post('/api/auth/register', json=user_data)
        assert response2.status_code == 400
        assert 'username' in response2.json['error'].lower()
    
    def test_register_duplicate_email(self, client, app_context):
        """Test registration with duplicate email"""
        user_data = {
            'username': 'testuser1',
            'email': 'test@example.com',
            'password': 'TestPass123',
            'first_name': 'John',
            'last_name': 'Doe'
        }
        
        # First registration
        response1 = client.post('/api/auth/register', json=user_data)
        assert response1.status_code == 201
        
        # Second registration with same email
        user_data['username'] = 'testuser2'
        response2 = client.post('/api/auth/register', json=user_data)
        assert response2.status_code == 409
        assert 'email' in response2.json['error'].lower()
    
    def test_register_invalid_name(self, client):
        """Test registration with invalid names"""
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'TestPass123',
            'first_name': 'J',  # Too short
            'last_name': 'Doe'
        }
        response = client.post('/api/auth/register', json=data)
        assert response.status_code == 400

class TestUserLogin:
    """Unit tests for user login"""
    
    def test_login_valid_credentials(self, client, app_context):
        """Test login with valid credentials"""
        # Create user
        user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'TestPass123',
            'first_name': 'John',
            'last_name': 'Doe'
        }
        client.post('/api/auth/register', json=user_data)
        
        # Login
        login_data = {
            'username': 'testuser',
            'password': 'TestPass123'
        }
        response = client.post('/api/auth/login', json=login_data)
        assert response.status_code == 200
        assert 'access_token' in response.json
        assert response.json['user']['username'] == 'testuser'
    
    def test_login_invalid_password(self, client, app_context):
        """Test login with invalid password"""
        # Create user
        user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'TestPass123',
            'first_name': 'John',
            'last_name': 'Doe'
        }
        client.post('/api/auth/register', json=user_data)
        
        # Login with wrong password
        login_data = {
            'username': 'testuser',
            'password': 'WrongPass123'
        }
        response = client.post('/api/auth/login', json=login_data)
        assert response.status_code == 401
    
    def test_login_nonexistent_user(self, client):
        """Test login with nonexistent user"""
        login_data = {
            'username': 'nonexistent',
            'password': 'TestPass123'
        }
        response = client.post('/api/auth/login', json=login_data)
        assert response.status_code == 401
    
    def test_login_missing_credentials(self, client):
        """Test login with missing credentials"""
        response = client.post('/api/auth/login', json={})
        assert response.status_code == 400
        assert 'required' in response.json['error'].lower()

class TestUserOperations:
    """Unit tests for user operations"""
    
    def test_get_user_unauthenticated(self, client):
        """Test getting user details without authentication"""
        response = client.get('/api/users/1')
        assert response.status_code == 401
    
    def test_list_users_unauthenticated(self, client):
        """Test listing users without authentication"""
        response = client.get('/api/users')
        assert response.status_code == 401
