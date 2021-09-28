from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_mail import Mail
from flask_login import LoginManager
from instance.config import DevelopmentConfig, TestingConfig, ProductionConfig


# Create the Flask app with defined paths for templete and static files
app = Flask(__name__,
            static_url_path='',
            static_folder='static',
            template_folder='templates'
            )

# Assign the app configuration based on the running envioroment
if app.config['ENV'] == "production":
    app.config.from_object(ProductionConfig)
elif app.config['ENV'] == "testing":
    app.config.from_object(TestingConfig)
else:
    app.config.from_object(DevelopmentConfig())

# Define Flask extensions for the app
db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app, db)
mail = Mail(app)

# Define the sessions login manager
login_manager = LoginManager(app)
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth_bp.login'


from lps.models import User
from lps.cli import *


# VIEW ROUTES
@app.route('/', methods=["GET"])
def index():
    return render_template('index.html'), 200


# Import auth blueprint
from lps.auth.routes import auth_bp
app.register_blueprint(auth_bp)


# Import api blueprint
from lps.api.routes import api_bp
app.register_blueprint(api_bp)


# Import map blueprint
from lps.map.routes import map_bp
app.register_blueprint(map_bp)
