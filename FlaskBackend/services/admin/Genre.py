import mysql.connector
from flask import Flask, jsonify, request
import pymysql
from flask import Blueprint, request, jsonify
genre_bp = Blueprint('genre_bp', __name__)

app = Flask(__name__)

# Establish MySQL connection
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="moviecrud"
)
# Insert genre of movies into the Genre table
@genre_bp.route('/genre', methods=['POST'])
def addGenre():
    try:
        # Get the JSON data from the request
        json = request.json
        genre = json.get('genre')

        if genre:
            # Create SQL query and bind data
            sqlQuery = "INSERT INTO genre (genre) VALUES (%s)"
            bindData = (genre,)
            
            # Use the existing connection and execute the query
            cursor = mydb.cursor()
            cursor.execute(sqlQuery, bindData)
            mydb.commit()
            
            response = jsonify('Genre added successfully')
            response.status_code = 200
            return response
        else:
            return jsonify('Genre field is missing'), 400
    except KeyError:
        # Return an error message if a mandatory field is missing in the JSON data
        return jsonify('One value is missing. All fields are mandatory'), 400

# Delete a particular genre
@genre_bp.route('/genre/<int:genreid>', methods=['DELETE'])
def deleteGenre(genreid):
    try:
        # Check if the genre exists
        cursor = mydb.cursor()
        cursor.execute("SELECT genre FROM genre WHERE genreid = %s", (genreid,))
        data = cursor.fetchone()

        if data is None:
            # If genre does not exist
            return jsonify('Genre does not exist'), 404
        
        # If genre exists, delete it
        cursor.execute("DELETE FROM genre WHERE genreid = %s", (genreid,))
        mydb.commit()
        
        response = jsonify('Genre deleted successfully!')
        response.status_code = 200
        return response
    except Exception as e:
        print(e)
        return jsonify('Something went wrong'), 500

# Get all genres
@genre_bp.route('/genre', methods=['GET'])
def viewGenre():
    try:
        # Get all genres from the database
        cursor = mydb.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT genreid, genre FROM genre")
        empRows = cursor.fetchall()
        response = jsonify(empRows)
        response.status_code = 200
        return response
    except Exception as e:
        print(e)
        return jsonify({'error': 'Error while retrieving genres from database'}), 500

if __name__ == '__main__':
    app.run(debug=True)
