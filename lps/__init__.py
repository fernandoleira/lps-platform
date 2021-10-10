from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from instance.config import DevelopmentConfig, TestingConfig, ProductionConfig
from lps.redis import RedisClient


# Define the Flask SQLAlchemy extension to cennect into the app database
db = SQLAlchemy()

# Define the Redis extension to cennect into the redis cache database
cache_db = RedisClient()

# Define the Flask Marshmellow extension to access the database schemas
ma = Marshmallow()

# Define the Flask Migrate extension to modify the app database structure
migrate = Migrate()

# Define the Flask Mail extension to send email notifications
mail = Mail()

# Define the Sessions Login Manager
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth_bp.login'


# Define the Flask app function with defined paths for templete and static files
def create_app(script_info=None):
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
        app.config.from_object(DevelopmentConfig)

    # Init extensions
    db.init_app(app)
    cache_db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    login_manager.init_app(app)

    # VIEW ROUTES
    from lps.home import home
    app.register_blueprint(home.home_bp)

    # Import auth blueprint
    from lps.auth import auth
    app.register_blueprint(auth.auth_bp)

    # Import api blueprint
    from lps.api import api
    app.register_blueprint(api.api_bp)

    # Import map blueprint
    from lps.map import map
    app.register_blueprint(map.map_bp)

    # Shell context for flask cli
    app.shell_context_processor({'app': app, 'db': db})
    
    return app
