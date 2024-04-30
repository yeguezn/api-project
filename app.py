from flask import Flask, redirect
from routes.users import users
from routes.auth_users import users_authentication
from routes.applications import applications
from routes.authorize_users import users_authorization
from routes.admin import admin
from routes.queries import queries
from config import configure
import os
from flask_swagger_ui import get_swaggerui_blueprint
from db.connection import create_database

configure()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
create_database()

SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'

SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "API autenticación"
    }
)

create_database()

@app.route("/")
def index():
    return redirect("http://localhost:5000/swagger")

#Registering routes
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
app.register_blueprint(users)
app.register_blueprint(users_authentication)
app.register_blueprint(applications)
app.register_blueprint(users_authorization)
app.register_blueprint(admin)
app.register_blueprint(queries)

if __name__ == "__main__":
	
	app.run(host="0.0.0.0")