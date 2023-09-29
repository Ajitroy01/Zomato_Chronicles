import pytest
from app import create_app  # Import your app and db instance
from app.models import User, Order, db  # Import your Dish model

# Define a fixture to set up the testing environment
@pytest.fixture
def app():
    app = create_app(config_name="test")  # Use a testing configuration
    with app.app_context():
        db.create_all()  # Create the testing database
        yield app
        db.session.remove()
        db.drop_all()

# Define a fixture to get a test client
@pytest.fixture
def client(app):
    return app.test_client()


def test_customer_signup(client):
    # Test customer signup
    response = client.post('/customer-signup', json={
        'username': 'john_doe',
        'password': 'password',
        'customer_name': 'John Doe',
        'address': '123 Main St'
    })
    assert response.status_code == 201
    assert b"Account created successfully" in response.data

def test_staff_signup(client):
    # Test staff signup
    response = client.post('/staff-signup', json={
        'username': 'staff_user',
        'password': 'password'
    })
    assert response.status_code == 201
    assert b"Staff account created successfully" in response.data

def test_customer_login(client):
    # Test customer login
    client.post('/customer-signup', json={
        'username': 'john',
        'password': '1234',
        'customer_name': 'John Doe',
        'address': '123 Main St'
    })

    response = client.post('/customer-login', json={
        'username': 'john',
        'password': '1234'
    })
    assert response.status_code == 200
    assert b"Logged in successfully" in response.data

def test_staff_login(client):
    # Test staff login
    client.post('/staff-signup', json={
        'username': 'user',
        'password': '1234'
    })

    response = client.post('/staff-login', json={
        'username': 'user',
        'password': '1234'
    })
    assert response.status_code == 200
    assert b"Staff logged in successfully" in response.data

def test_logout(client):
    # Test logout
    client.post('/customer-signup', json={
        'username': 'john_doe',
        'password': 'password',
        'customer_name': 'John Doe',
        'address': '123 Main St'
    })

    client.post('/customer-login', json={
        'username': 'john_doe',
        'password': 'password'
    })

    response = client.post('/logout')
    assert response.status_code == 200
    assert b"Logged out successfully" in response.data
