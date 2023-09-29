from flask import Blueprint, request, jsonify
from flask_login import current_user, login_required
from app.models import db,Dish, Order, User

staff_bp = Blueprint('staff', __name__)

@staff_bp.route('/menu/update_availability/<int:dish_id>', methods=['PUT'])
def update_availability(dish_id):
    # Check if the dish exists
    dish = db.session.get(Dish, dish_id)
    if not dish:
        return jsonify({'error': 'Dish not found'}), 404

    # Parse the JSON request data to get the new availability status
    data = request.get_json()
    new_availability = data.get('availability')

    # Update the dish's availability
    dish.availability = new_availability
    db.session.commit()

    return jsonify({'message': 'Dish availability updated successfully'}), 200

@staff_bp.route('/orders/take', methods=['POST'])
def take_order():
    # Parse the JSON request data to get order details
    data = request.get_json()
    customer_id = data.get('customer_id')  # Use customer_id instead of customer_name
    dish_ids = data.get('dish_ids')

    # Initialize a list to store ordered dishes
    ordered_dishes = []

    # Check the availability of each dish and add it to the ordered_dishes list
    for dish_id in dish_ids:
        dish = db.session.get(Dish, dish_id)

        if not dish:
            return jsonify({'error': f'Dish with ID {dish_id} not found'}), 404

        if not dish.availability:
            return jsonify({'error': f'Dish "{dish.name}" is not available'}), 400

        ordered_dishes.append(dish)

    # Create a new order and add ordered dishes to it
    order = Order(customer_id=customer_id, status='received')  # Use customer_id instead of customer_name
    order.dishes.extend(ordered_dishes)

    # Commit the order to the database
    db.session.add(order)
    db.session.commit()

    return jsonify({'message': 'Order taken successfully', 'order_id': order.id}), 200


@staff_bp.route('/orders/update_status/<int:order_id>', methods=['PUT'])
def update_order_status(order_id):
    # Check if the order exists
    order = db.session.get(Order, order_id)
    if not order:
        return jsonify({'error': 'Order not found'}), 404

    # Parse the JSON request data to get the new order status
    data = request.get_json()
    new_status = data.get('status')

    # Define the valid order status transitions
    status_transitions = {
        'received': ['preparing'],
        'preparing': ['ready for pickup'],
        'ready for pickup': ['delivered'],
        'delivered': [],  # No further transitions allowed
    }

    # Check if the new status is a valid transition from the current status
    if new_status not in status_transitions.get(order.status, []):
        return jsonify({'error': 'Invalid status transition'}), 400

    # Update the order's status
    order.status = new_status
    db.session.commit()

    return jsonify({'message': 'Order status updated successfully'}), 200

@staff_bp.route('/orders/review', methods=['GET'])
def review_orders():
    # Retrieve all orders
    orders = Order.query.all()

    # Prepare a list of order details to return
    order_details = []
    for order in orders:
        # Retrieve the customer's username and address based on customer_id
        customer = User.query.filter_by(id=order.customer_id).first()
        
        order_details.append({
            'order_id': order.id,
            'customer_name': customer.customer_name,  # Use customer_name from User model
            'customer_address': customer.address,  # Include customer's address
            'dishes': [dish.name for dish in order.dishes],
            'status': order.status,
        })

    return jsonify({'orders': order_details}), 200

@staff_bp.route('/customer-orders/<int:customer_id>', methods=['GET'])
@login_required
def get_customer_orders(customer_id):
    try:
        # Check if the current user is a customer and has the same ID as the requested customer_id
        if current_user.is_authenticated and current_user.role == 'customer' and current_user.id == customer_id:
            # Query orders for the specific customer
            orders = Order.query.filter_by(customer_id=customer_id).all()

            # Serialize the list of orders into JSON format
            order_list = [order.serialize() for order in orders]

            return jsonify({'orders': order_list}), 200
        else:
            return jsonify({'message': 'Unauthorized', 'success': False}), 401

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@staff_bp.route('/exit', methods=['GET'])
def exit_app():
    # Optionally, you can return a message indicating the exit process has started
    return jsonify({'message': 'Exiting the application'}), 200