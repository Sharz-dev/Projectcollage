from functools import wraps
from flask import request,jsonify
import jwt
from app import app

def jwtauth(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        # Get the access token from the Authorization header of the request
        acess_tocken = request.headers.get('Authorization')
         # Remove the 'Bearer ' prefix from the access token
        acess_tocken = acess_tocken.replace('Bearer ', '')
        # Check if the access token is missing
        if not acess_tocken:
            return jsonify({'message': 'Missing token!'}), 403
        try:
            # Verify and decode the access token using the JWT_SECRET_KEY
            jwt.decode(acess_tocken, app.config['JWT_SECRET_KEY'], algorithms='HS256')
            print(acess_tocken) 
        except:
            # If the access token is invalid, return an error message
            return jsonify({'message': 'Invalid token!'}), 403 
        # If the access token is valid, call the function with the given arguments 
        return func(*args, **kwargs)
    # Return the wrapped function
    return wrapped
