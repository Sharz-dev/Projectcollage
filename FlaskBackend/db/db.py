from socket import fromshare
import mysql.connector
from flask import Flask
import bcrypt
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
# app = Flask(__name__)
# CORS(app)

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="moviecrud"
)
# db_Create_Table_Query = """CREATE TABLE genre
# (
#     genreid int(100) not null auto_increment,
#     genre varchar(50) not null,
#     CONSTRAINT genre_pk PRIMARY KEY (genreid)
# )"""
# #Creating table for movies
# db_Create_Table_Query = """CREATE TABLE movies
# (
#   movieid int(100) not null auto_increment PRIMARY KEY,
#   moviename varchar(50) not null,
#   moviegenre int(100) not null,
#   director varchar(100) not null,
#   language varchar(50) not null,
#   FOREIGN KEY (moviegenre) REFERENCES genre(genreid)
# )"""

#Creating Tables for role

# db_Create_Table_Query = """CREATE TABLE role
# (
#     roleid int(100) not null auto_increment,
#     role varchar(50) not null,
#     CONSTRAINT role_pk PRIMARY KEY (roleid)
#  )"""


# #creating table for user

# db_Create_Table_Query = """CREATE TABLE user
# (
#   userid int(100) not null auto_increment PRIMARY KEY,
#   fullname varchar(50) not null,
#   username varchar(50) not null,
#   password varchar(50) not null,
#   usertype int(100) not null,
#   FOREIGN KEY (usertype) REFERENCES role(roleid)
#  )"""

# db_Create_Table_Query = """CREATE TABLE rating
# (
#     rateid int(100) not null auto_increment PRIMARY KEY,
#     userid int(100) not null,
#     movieid int(100) not null,
#     rating int(100) not null,
#     FOREIGN KEY (userid) REFERENCES user(userid),
#     FOREIGN KEY (movieid) REFERENCES movies(movieid)
#     )"""



# cursor = mydb.cursor()
# result = cursor.execute(db_Create_Table_Query)
# print("  table created successfully ")
# # # result = cursor.execute(genre_table_query)
# # print(" Genre table created successfully ")
# # # result = cursor.execute(role_table_query)
# # print(" Role table created successfully ")
# # result = cursor.execute(user_table_query)
# # print(" User table created successfully ")

# # result = cursor.execute(rating_Table_Query)
# # print(" Rating table created successfully ")

