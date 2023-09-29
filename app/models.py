from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

# Define an association table to manage the many-to-many relationship
order_dish_association = db.Table('order_dish_association',
    db.Column('order_id', db.Integer, db.ForeignKey('orders.id')),
    db.Column('dish_id', db.Integer, db.ForeignKey('dishes.id'))
)

class Dish(db.Model):
    __tablename__ = 'dishes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    availability = db.Column(db.Boolean, default=True)
    image = db.Column(db.String(255))  # Add the "image" column for storing image URL
    description = db.Column(db.Text)   # Add the "description" column for describing dishes

    def __init__(self, name, price, availability=True, image=None, description=None):
        self.name = name
        self.price = price
        self.availability = availability
        self.image = image
        self.description = description

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'availability': self.availability,
            'image': self.image,          # Include image URL in serialization
            'description': self.description  # Include description in serialization
        }

    def save(self):
        db.session.add(self)
        db.session.commit()


class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) 
    status = db.Column(db.String(50), default='received', nullable=False)

    # Define the many-to-many relationship between Order and Dish
    dishes = relationship('Dish', secondary=order_dish_association, backref='orders', lazy=True)

    def __init__(self, customer_id, status='received'):
        self.customer_id = customer_id
        self.status = status

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'staff' or 'customer'

    # Customer-specific fields
    customer_name = db.Column(db.String(100))  # Add any other customer-specific fields as needed
    address = db.Column(db.String(255))

    def __init__(self, username, password, role, customer_name=None, address=None):
        self.username = username
        self.password = password
        self.role = role
        self.customer_name = customer_name
        self.address = address