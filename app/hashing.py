from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

def hash_password(password):
    """
    Hashes a password and returns the hashed string.
    """
    return bcrypt.generate_password_hash(password).decode('utf-8')

def check_password(hashed_password, password_to_check):
    """
    Checks if a password matches its hashed version.
    """
    return bcrypt.check_password_hash(hashed_password, password_to_check)
