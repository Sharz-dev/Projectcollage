from models.Movie import Movie
import pymysql
import mysql.connector
from app import app
from flask import Blueprint, request, jsonify
# from services.services import execute,commitConnection
import logging
from services.Logger import *
from services.Auth import *
from flask import make_response
from flask_cors import CORS
CORS(app, resources={r"/movie": {"origins": "http://localhost:3000"}})

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="moviecrud"
)

movie_bp = Blueprint('movie_bp', __name__)
# insert Movie details into movie table
@movie_bp.route('/movie', methods=['POST'])
def createMovie(movieid=None):
    try:
        # Extracting the movie details from the JSON data in the request object
        json = request.json
        moviename = json.get('moviename') 
        check_For_String(moviename)  # Checking if 'moviename' is a string
        check_For_Empty_String(moviename)  # Checking if 'moviename' is not an empty string

        moviegenre = json.get('moviegenre')
        check_For_String(moviegenre)
        check_For_Empty_String(moviegenre)

        language = json.get('language')
        check_For_String(language)
        check_For_Empty_String(language)

        director = json.get('director')
        check_For_Empty_String(director)

        # Calling the function to add the movie to the database
        return addMovie(movieid,moviename, moviegenre, language, director, request)

    except KeyError as e:
        logger.error(f"KeyError: {e}")
        return jsonify({'message': 'Some columns are missing or misspelled the column name'}), 400
    except ValueError as e:
        # Catching errors if any of the mandatory fields are empty
        logger.error(f"ValueError: {e}")
        return jsonify({'message': str(e)}), 400
    except Exception as e:
        # Catching other exceptions
        logger.error(f"Exception: {e}")
        return jsonify({'message': 'Something went wrong..!!'}), 500
    
# delete movie from table movie
@movie_bp.route('/movie/<movieid>', methods=['DELETE'])
# @jwtauth  # Uncomment this if you're using JWT authentication
def deletemovie(movieid):
    try:
        # SQL query to check if the movie exists
        sqlQuery = "SELECT moviename FROM movies WHERE movieid = %s"
        bindData = (movieid,)  # Use tuple for bind data
        conn = mydb  # Use the existing connection (do not create a new one)
        cursor = conn.cursor(dictionary=True)
        
        # Execute the query to check if the movie exists
        cursor.execute(sqlQuery, bindData)
        movie = cursor.fetchone()  # Fetch one row

        if movie is None:
            # Movie does not exist
            return jsonify({'message': 'Movie does not exist'}), 404

        # SQL query to delete the movie
        sqlQuery = "DELETE FROM movies WHERE movieid = %s"
        
        # Execute the delete query
        cursor.execute(sqlQuery, bindData)
        conn.commit()  # Commit the transaction

        # Return success response
        return jsonify({'message': 'Movie deleted successfully!'}), 200

    except Exception as e:
        # Log the error and return a generic error response
        logger.error(f"Error occurred while deleting the movie: {e}")
        return jsonify({'message': f"Error occurred: {str(e)}"}), 500


    
            
# Update movie details by movie id
@movie_bp.route('/movie/<movieid>', methods=['PUT'])
# @jwtauth  # If authentication is required, uncomment this decorator
def updateMovie(movieid):
    try:
        # Get movie details from the request body
        data = request.json
        newId = movieid
        newName = data['moviename']
        newGenre = data['moviegenre']
        newDirector = data['director']
        newLanguage = data['language']
        
        movie = Movie(newId, newName, newGenre, newDirector, newLanguage)

        # Check if all required fields are present
        if newId and newName and newGenre and newDirector and newLanguage and request.method == 'PUT':
            
            # Check if movie exists in the database
            query = "SELECT COUNT(*) FROM movies WHERE movieid=%s"
            conn = mydb
            cursor = conn.cursor()

            cursor.execute(query, (movieid,))
            result = cursor.fetchone()
            movie_exists = result[0] > 0

            if not movie_exists:
                return jsonify('Movie does not exist'), 404

            # If movie exists, update the movie details
            update_query = """
                UPDATE movies 
                SET moviename=%s, moviegenre=%s, director=%s, language=%s 
                WHERE movieid=%s
            """
            update_data = (movie.moviename, movie.moviegenre, movie.director, movie.language, movie.movieid)

            cursor.execute(update_query, update_data)
            conn.commit()

            return jsonify('Movie updated successfully!'), 200

        else:
            return jsonify('Some required fields are missing or the method is incorrect'), 400

    except KeyError as e:
        logger.error(f"KeyError: {e}")
        return jsonify('Some Columns are missing or mispelled the column name'), 400
    except ValueError as e:
        logger.error(f"ValueError: {e}")
        return jsonify(str(e)), 400
    except Exception as e:
        logger.error(f"Exception: {e}")
        return jsonify('Something went wrong..!!'), 500

# view all Movies from movie table
@movie_bp.route('/movie', methods=['GET'])
# @jwtauth
def viewMovies():
    try:
        cursor = mydb.cursor(dictionary=True)
        cursor.execute("SELECT movies.movieid,movies.moviename, genre.genre, movies.director, movies.language FROM movies JOIN genre ON movies.moviegenre = genre.genreid;")
        empRows = cursor.fetchall()
        # commitConnection()
        response = jsonify(empRows)
        response.status_code = 200
        return response
    except Exception as e:
        print(e)
        return jsonify({'error': 'Error while retrieving movies from database'})

        
# view particular movies from movie table

@movie_bp.route('/movie/<movieid>', methods=['GET'])
# Decorator to perform JWT authentication
# @jwtauth
def movieDetail(movieid, moviename=None, moviegenre=None, director=None, language=None):
    try:
        movie = Movie(movieid,moviename, moviegenre, director, language)
        cursor = mydb.cursor(dictionary=True)
        sqlQuery = ("SELECT movies.movieid, genre.genre, movies.director, movies.language FROM movies JOIN genre ON movies.moviegenre = genre.genreid WHERE movieid= %s")
        bindData = (movie.movieid,)
        # cursor.execute(sqlQuery, bindData)
        cursor.execute(sqlQuery, bindData)
        empRow = cursor.fetchone()
        if empRow:
            response = jsonify(empRow)
            response.status_code = 200
            return response
        else:
            return jsonify({'error': 'Movie not found'}), 404

    except Exception as e:
        return jsonify({'error': f'Error while retrieving movie: {str(e)}'}), 500
# Viewrating
# @app.route('/movies', methods=['GET'])
# # Decorator to perform JWT authentication
# @jwtauth
# def viewMovierating():
#     try:
#         conn = mydb.connect()
#         cursor = conn.cursor(pymysql.cursors.DictCursor)
#         cursor.execute("SELECT movies.movieid, movies.moviename, AVG(rating.rating) AS rating, genre.genre, movies.director, movies.language FROM rating INNER JOIN movies ON movies.movieid = rating.movieid INNER JOIN genre ON movies.moviegenre = genre.genreid GROUP BY movies.movieid, movies.moviename;")

#         empRows = cursor.fetchall()
#         conn.commit()
#         # commitConnection()
#         response = jsonify(empRows)
#         response.status_code = 200
#         return response
#     except Exception as e:
#         print(e)
#         return jsonify({'error': 'Error while retrieving movies from database'})
        

# error handling
@app.errorhandler(404)
def showMessage(error=None):
    message = {
        'status': 404,
        'message': 'Record not found: ' + request.url,
    }
    respone = jsonify(message)
    respone.status_code = 404
    return respone

#function to check the values are in string
def check_For_String(value):
    if not isinstance(value, str):
        raise ValueError(f"{value} should be a string")
    
#function to check the values are empty or not
def check_For_Empty_String(value):
    if not value or not value.strip():
        raise ValueError(f"{value} cannot be empty or only whitespace")

#Function for recalling
def addMovie(moviename, moviegenre, language, director, request):
    if not moviename or not moviegenre or not language or not director:
        response = make_response(jsonify({'message': 'All fields are required'}))
        response.status_code = 400
        return response

    movie = Movie(moviename=moviename, moviegenre=moviegenre, language=language, director=director)

    if request.method == 'POST':
        sqlQuery = "INSERT INTO movies(moviename, moviegenre, language, director) VALUES( %s, %s, %s, %s)"
        bindData = (movie.moviename, movie.moviegenre, movie.language, movie.director)
        
        try: # Open the DB connection
            mydb = mysql.connector.connect(
            host="localhost",
             user="root",
            password="",
            database="moviecrud"
            )
            cursor = mydb.cursor(dictionary=True)
            # Execute SQL query
            cursor.execute(sqlQuery, bindData)

            # Commit the transaction
            mydb.commit()

            # Close the cursor and connection
            return jsonify({'message': 'Movie created successfully'}), 201


        except pymysql.MySQLError as e:
            logger.error(f"MySQL Error: {e}")
            return jsonify({'message': 'Database error occurred'}), 500
        except Exception as e:
            logger.error(f"Exception: {e}")
            return jsonify({'message': 'Something went wrong while adding the movie',},e), 500