import pytest
from app import create_app  # Import your app and db instance
from app.models import Dish, db  # Import your Dish model

# Define a fixture to set up the testing environment
@pytest.fixture
def app():
    app = create_app(config_name="test")  # Use a testing configuration
    with app.app_context():
        db.create_all()  # Create the testing database
        yield app

# Define a fixture to get a test client
@pytest.fixture
def client(app):
    return app.test_client()

# Test cases for the menu_bp endpoints
def test_get_menu(client):
    response = client.get('/menu')
    assert response.status_code == 200
    # Add assertions to check the response JSON data

def test_add_dish(client):
    # Create a JSON data payload for adding a dish
    data = {
        'name': 'New Dish',
        'price': 10.99,
        'availability': True,
        'image': 'image_url',
        'description': 'A new dish description',
    }
    response = client.post('/menu/add', json=data)
    assert response.status_code == 200
    # Add assertions to check the response message and data in the database

def test_update_dish(client):
    # Create a JSON data payload for updating a dish
    data = {
        'name': 'Updated Dish',
        'price': 12.99,
        'availability': False,
        'image': 'new_image_url',
        'description': 'An updated dish description',
    }
    response = client.put('/menu/update/1', json=data)
    assert response.status_code == 200
    # Add assertions to check the response message and data in the database

def test_get_dish(client):
    response = client.get('/menu/1')
    assert response.status_code == 200
    # Add assertions to check the response JSON data

def test_delete_dish(client):
    response = client.delete('/menu/delete/1')
    assert response.status_code == 200
    # Add assertions to check the response message and data in the database
