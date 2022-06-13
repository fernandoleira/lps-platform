from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_cors import CORS
from flask_mail import Mail
from instance.config import DevelopmentConfig, TestingConfig, ProductionConfig
from api.redis import RedisClient


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


# Define the Flask app function with defined paths for templete and static files
def create_app(script_info=None):
    app = Flask(__name__, static_url_path='', static_folder='static', template_folder='templates')

    # Assign the app configuration based on the running envioroment
    if app.config['ENV'] == 'production':
        app.config.from_object(ProductionConfig)
    elif app.config['ENV'] == 'testing':
        app.config.from_object(TestingConfig)
    else:
        app.config.from_object(DevelopmentConfig)

    # Init extensions
    db.init_app(app)
    cache_db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    #login_manager.init_app(app)

    # Setup CORS configuration
    CORS(app, resources={r"/api/*": {'origins': '*'}})

    # Import api blueprint
    from api.routes import api_bp
    app.register_blueprint(api_bp)

    # Import custom app shell commands and context for flask cli
    from api.cli import api_cli
    app.cli.add_command(api_cli)
    app.shell_context_processor({'app': app, 'db': db})
    
    return app
