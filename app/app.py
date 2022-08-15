from flask import Flask
from pymodm.connection import connect
from datetime import timedelta
from flask_jwt_extended import JWTManager


import config
import views.auth as auth
import views.board as board

app = Flask(__name__)
app.config["SECRET_KEY"] = "d06300c98fd89eaa08a1838356267a86"


# Connect to MongoDB
connect("mongodb://localhost:27017/flask_db2", alias="flask_app")

app.config["JWT_SECRET_KEY"] = "d06300c98fd89eaa08a1838356267a86" 
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = config.ACCESS_EXPIRES
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=31)
jwt = JWTManager(app)


# auth routes
app.add_url_rule('/login', view_func=auth.login, methods=['POST'])
app.add_url_rule('/refresh', view_func=auth.refresh, methods=['POST'])
app.add_url_rule('/singup', view_func=auth.signup, methods=['POST'])
app.add_url_rule('/logout', view_func=auth.logout, methods=['DELETE'])
# board routes
app.add_url_rule('/board', view_func=board.create_board, methods=['POST'])
app.add_url_rule('/get_board/<id>', view_func=board.get_board, methods=['GET'])
app.add_url_rule('/get_board', view_func=board.get_user_boards, methods=['GET'])
app.add_url_rule('/board/<id>', view_func=board.update_board, methods=['PUT'])



if __name__ == "__main__":
    app.run(debug = True)