import re
from flask import jsonify

def validate_password_strength(password):
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    if not re.search("[a-z]", password):
        return False, "Password must contain at least one lowercase letter"
    if not re.search("[A-Z]", password):
        return False, "Password must contain at least one uppercase letter"
    if not re.search("[0-9]", password):
        return False, "Password must contain at least one digit"
    if not re.search("[!@#$%^&*()_+=-]", password):
        return False, "Password must contain at least one special character (!@#$%^&*()_+=-)"
    return True, "Password is strong"

def validateRegisterData(name, user, password):
    if not name:
        return jsonify({"error": "Full name is required"}), 400
    if len(name) < 3:
        return jsonify({"error": "Full name must be at least 3 characters"}), 400
    if not all(i.isalpha() or i.isspace() for i in name):
        return jsonify({"error": "Full name can only contain letters and spaces"}), 400
    if not user:
        return jsonify({"error": "Username is required"}), 400
    if len(user) < 3:
        return jsonify({"error": "Username must be at least 3 characters"}), 400
    if not password:
        return jsonify({"error": "Password is required"}), 400
    password_is_strong, password_error = validate_password_strength(password)
    if not password_is_strong:
        return jsonify({"error": password_error}), 400
    return None
def validateLoginData( username, password):
    if not username:
        return jsonify({"error": "Username is required"}), 400
    if not password:
        return jsonify({"error": "Password is required"}), 400

