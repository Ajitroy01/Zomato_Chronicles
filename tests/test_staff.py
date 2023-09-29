import pytest
import json
from app import create_app
from app.models import Dish, Order, User, db

@pytest.fixture
def app():
    app = create_app(config_name="test")
    with app.app_context():
        db.create_all()  # Create the test database
        yield app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def init_database(app):
    # Create some sample dishes in the test database
    with app.app_context():
        dish1 = Dish(name='Spaghetti Carbonara', price=12.99, availability=True, image='image.url', description='desc')
        dish2 = Dish(name='Pizza Margherita', price=10.99, availability=True, image='image.url', description='desc')

        # Add and commit the dishes to the database
        db.session.add(dish1)
        db.session.add(dish2)
        db.session.commit()

    yield db  # This allows the tests to use the initialized database

    # Clean up the database after the tests
    with app.app_context():
        db.session.remove()
        db.drop_all()

def test_update_availability(client, init_database):
    # Test updating the availability of a dish
    response = client.put('/menu/update_availability/1', json={
        'availability': False
    })
    assert response.status_code == 200
    assert b"Dish availability updated successfully" in response.data

def test_take_order(client, init_database):
    # Create a customer in the database
    customer = User(username='john_doe', password='password', role='customer', customer_name='John Doe', address='New York')
    db.session.add(customer)
    db.session.commit()

    # Create dishes in the database with IDs 1 and 2
    dish1 = Dish(name='Spaghetti Carbonara', price=12.99, availability=True, image='image.url', description='desc')
    dish2 = Dish(name='Pizza Margherita', price=10.99, availability=True, image='image.url', description='desc')
    db.session.add(dish1)
    db.session.add(dish2)
    db.session.commit()

    # Log in as the customer
    client.post('/customer-login', json={
        'username': 'john_doe',
        'password': 'password'
    })

    # Test taking an order
    response = client.post('/orders/take', json={
        'customer_id': 1,  # Use customer_id instead of customer_name
        'dish_ids': [2, 3]
    })
    assert response.status_code == 200
    assert b"Order taken successfully" in response.data


def test_review_orders(client, init_database):
    # Test reviewing customer orders
    response = client.get('/orders/review')
    assert response.status_code == 200


# Define a test for retrieving customer orders
def test_get_customer_orders(client):
    # Register a customer user through the signup endpoint (you can use your existing signup test)
    response_signup = client.post('/customer-signup', json={
        'username': 'test_customer',
        'password': 'test_password',
        'customer_name': 'Test Customer',
        'address': '123 Test St'
    })
    assert response_signup.status_code == 201

    # Log in with the registered customer user
    response_login = client.post('/customer-login', json={
        'username': 'test_customer',
        'password': 'test_password'
    })
    assert response_login.status_code == 200

    # Retrieve orders for the authenticated customer
    response_orders = client.get('/customer-orders/1')  # Assuming customer_id is 1
    assert response_orders.status_code == 200

    # Ensure that the response contains the expected data (you can customize this based on your API response)
    data = json.loads(response_orders.data)
    assert 'orders' in data
    assert isinstance(data['orders'], list)


def test_update_order_status_valid_transition(client, init_database):
    sample_order = Order(
        customer_id=1,
        status='received'
    )
    init_database.session.add(sample_order)
    init_database.session.commit()

    valid_transition = {
        'status': 'preparing'
    }

    response = client.put('/orders/update_status/1', json=valid_transition)

    assert response.status_code == 200

    data = json.loads(response.data)
    assert 'message' in data
    assert data['message'] == 'Order status updated successfully'

    updated_order = db.session.get(Order, 1)
    assert updated_order.status == 'preparing'


def test_exit_app(client):
    # Test exiting the application
    response = client.get('/exit')
    assert response.status_code == 200
    assert b"Exiting the application" in response.data
