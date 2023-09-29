from flask_sqlalchemy import SQLAlchemy
from flask import Blueprint, request, jsonify

# Import the Dish model or your equivalent
from app.models import Dish, Order, db

menu_bp = Blueprint("menu", __name__)


@menu_bp.route('/menu', methods=['GET'])
def get_menu():
    try:
        # Query all dishes from the database
        dishes = Dish.query.all()
        
        # Serialize the list of dishes into JSON format
        dish_list = [dish.serialize() for dish in dishes]

        # Return the list of dishes as JSON response
        return jsonify({'menu': dish_list}), 200

    except Exception as e:
        # Handle any exceptions or errors
        return jsonify({'error': str(e)}), 500
    
@menu_bp.route("/menu/add", methods=["POST"])
def add_dish():
    try:
        data = request.get_json()
        # Create a new dish based on the JSON data and save it to the database
        new_dish = Dish(
            name=data['name'],
            price=data['price'],
            availability=data['availability'],
            image=data.get('image'),  # Include 'image' from JSON data
            description=data.get('description')  # Include 'description' from JSON data
        )
        db.session.add(new_dish)
        db.session.commit()
        return jsonify(message="Dish added successfully"), 200
    except Exception as e:
        # Handle any exceptions or errors
        return jsonify({'error': str(e)}), 500

@menu_bp.route("/menu/update/<int:dish_id>", methods=["PUT"])
def update_dish(dish_id):
    try:
        data = request.get_json()
        # Retrieve the dish from the database based on dish_id
        dish = db.session.get(Dish, dish_id)
        if dish:
            dish.name = data['name']
            dish.price = data['price']
            dish.availability = data['availability']
            # Update 'image' and 'description' if they exist in the JSON data
            if 'image' in data:
                dish.image = data['image']
            if 'description' in data:
                dish.description = data['description']
            db.session.commit()
            return jsonify(message="Dish updated successfully"), 200
        else:
            return jsonify(message="Dish not found"), 404
    except Exception as e:
        # Handle any exceptions or errors
        return jsonify({'error': str(e)}), 500


@menu_bp.route("/menu/<int:dish_id>", methods=["GET"])
def get_dish(dish_id):
    # Retrieve and return details of a dish based on dish_id
    dish = db.session.get(Dish, dish_id)
    if dish:
        return jsonify(dish.serialize()), 200
    else:
        return jsonify(message="Dish not found"), 404

@menu_bp.route("/menu/delete/<int:dish_id>", methods=["DELETE"])
def delete_dish(dish_id):
    # Delete a dish based on dish_id
    dish = db.session.get(Dish, dish_id)
    if dish:
        db.session.delete(dish)
        db.session.commit()
        return jsonify(message="Dish deleted successfully"), 200
    else:
        return jsonify(message="Dish not found"), 404
