from flask import Flask
from flask_cors import CORS
from services.admin.movie import movie_bp
from services.admin.Role import role_bp
from services.admin.Genre import genre_bp


from flask import Flask
from flask_cors import CORS
# from services.admin.movie import movie_bp
from services.user.users import user_bp

  # Import your Blueprint
# from services.user.users import user_bp

app = Flask(__name__)

# Enable CORS for all routes

CORS(app, origins="http://localhost:3000")
# Register your Blueprint
# app.register_blueprint(movie_bp)
app.register_blueprint(user_bp)
app.register_blueprint(role_bp)
app.register_blueprint(movie_bp)
app.register_blueprint(genre_bp)



if __name__ == "__main__":
    app.run(debug=True)
