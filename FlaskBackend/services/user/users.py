import bcrypt
from models.User import User
import jwt
import pymysql
import mysql.connector
# from config import mydb
from flask import jsonify
from flask import request,Blueprint
from app import app
from validation import validateRegisterData,validateLoginData
# registration of user, here datas are entered to user table
user_bp = Blueprint('user_bp', __name__)

secret_key="85a4634e40cc6e9493e59d2c3d86c81887bfd5fca1c1824222a467110170ecb4"

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="moviecrud"
)


@user_bp.route('/register', methods=['POST'])
def register():
    try:
        json = request.json
        name = json.get('fullname')
        username = json.get('username')
        password = json.get('password')
        usertype = "2"  # default usertype for regular users
        
        # Input validation (e.g. check for missing fields)
        if not name or not username or not password:
            return jsonify({"error": "Missing required fields"})

        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        cursor = mydb.cursor(dictionary=True)

        # Check if the user already exists
        query = "SELECT * FROM user WHERE username = %s"
        cursor.execute(query, (username,))
        existing_user = cursor.fetchone()
        
        if existing_user:
            cursor.close()
            return jsonify({"error": "User already exists!"})

        # Insert the new user into the database
        insert_query = "INSERT INTO user (fullname, username, password, usertype) VALUES (%s, %s, %s, %s)"
        cursor.execute(insert_query, (name, username, hashed_password, usertype))
        mydb.commit()  # Commit the changes
        cursor.close()
        
        return jsonify({"message": "User registered successfully!"})

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)})
    
# login function of user
@user_bp.route('/login', methods=['POST'])
def login(userid=None, fullname=None, usertype=None):
    try:
        # Get login data from the request body
        json = request.json
        name = json['username']
        password = json['password']
        
        # Validate login data (assumes validateLoginData is defined somewhere)
        validation_error = validateLoginData(name, password)
        if validation_error:
            return validation_error

        # Create a User object (optional in this case, but kept for structure)
        user = User(userid, fullname, name, password, usertype)

        # Ensure username and password are provided
        if name and password and request.method == 'POST':
            cursor = mydb.cursor(dictionary=True)  # Using dictionary cursor for easier access to columns
            query = "SELECT * FROM user WHERE username = %s"
            bindData = (user.username,)  # Ensure the data is in a tuple for the query

            cursor.execute(query, bindData)  # Execute the query
            row = cursor.fetchone()  # Fetch the first result (if any)

            if row:
                # Get the stored password from the database
                stored_password = row.get('password')
                usertype = row.get('usertype')

                # Compare the passwords using bcrypt
                if bcrypt.checkpw(user.password.encode('utf-8'), stored_password.encode('utf-8')):
                    # Create JWT token if login is successful
                    access_token = jwt.encode({'username': name},secret_key )
                    return jsonify(message='Login Successful', access_token=access_token ,usertype=usertype),200
                else:
                    return jsonify(message='Password is incorrect, Try again with the correct one..!!'), 401
            else:
                return jsonify(message='Bad username or password... Access Denied!'), 401
        else:
            return jsonify(message='Please provide both username and password!'), 400

    except KeyError as ke:
        return jsonify(message=f'Missing or incorrect key: {str(ke)}'), 400
    except Exception as e:
        print(e)
        return jsonify(message="An error occurred while processing the request"), 500


@user_bp.route('/test')
def test_db_connection():
    try:
        conn = mydb.connect()
        cursor = conn.cursor()
        cursor.execute('SELECT 1')
        return 'Database connected successfully'
    except Exception as e:
        return f'Error connecting to database: {e}'