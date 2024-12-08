from app import app
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from flask_mysqldb import MySQL

mydb = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'moviecrud'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
# jwt secret key for creating the jwt token
# app.config['JWT_SECRET_KEY'] = '3fc2063fd1334cc68ca265ea0c4c4b11'
mydb.init_app(app)
jwt = JWTManager(app)