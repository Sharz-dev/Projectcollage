from urllib import response
from models.Rating import Rating
import pymysql
from config import mydb
from flask import jsonify
from flask import request
from app import app
from services.Logger import *
from services.Auth import *

#add rating for a particular track by particular user, datas are added to table rating
@app.route('/rating', methods = ['POST'])
@jwtauth
def addRating(rateid=None):
    try:
        json = request.json
        userid = json['userid']
        movieid = json['movieid']
        rating = json['rating']
        rates = Rating(rateid,userid, movieid, rating)
        if userid and movieid and rating and request.method == 'POST' :
            conn = mydb.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            sqlQuery = "INSERT INTO rating(userid, movieid, rating) VALUES (%s, %s, %s)"
            bindData = (rates.userid, rates.movieid, rates.rating)
            cursor.execute(sqlQuery,bindData)
            conn.commit()
            response = jsonify('Rating added successfully!')
            response.status_code = 200
            return response
    except KeyError:
        return jsonify('value missing')
    except pymysql.IntegrityError as e:
        return jsonify('You are entering wrong userid or movieid , which is not in table..!!!')
    except Exception as e :
        print(e)
        return jsonify("error")

