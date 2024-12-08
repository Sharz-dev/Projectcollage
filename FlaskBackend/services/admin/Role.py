from models.Role import Role
import pymysql
from db.db import mydb
from flask import jsonify
from app import app
from flask import request,Blueprint
import mysql.connector
# from config import mydb

role_bp = Blueprint('role_bp', __name__)

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="moviecrud"
)

#Insert a Role to to Role Table
@role_bp.route('/addRole', methods=['POST'])
def addRole(roleid=None):
    try:
        # Get the role data from the request body
        json = request.json
        role = json['role']
        
        # Create a new Role object using the role data
        roleobj = Role(roleid, role)
        
        # Check if the role exists and the request method is POST
        if role and request.method == 'POST':
            cursor = mydb.cursor()  # Create a cursor object using the existing connection
            # Insert the new role into the role table
            sqlQuery = "INSERT INTO role (role) VALUES (%s)"
            bindData = (roleobj.role,)  # Tuple for the bind data
            cursor.execute(sqlQuery, bindData)
            mydb.commit()  # Commit the transaction to the database
            
            # Return a response indicating the role was added successfully
            response = jsonify({'message': 'Role is added successfully'})
            response.status_code = 200
            return response
        else:
            return jsonify({'message': 'Something went wrong'}), 400
    except KeyError:
        return jsonify({'message': 'Key error, one value is missing'}), 400
    except Exception as e:
        return jsonify({'message': str(e)}), 500