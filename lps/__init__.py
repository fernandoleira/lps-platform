from functools import wraps
from flask import Flask, render_template, request, redirect, jsonify, abort, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_mail import Mail, Message
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from instance.config import DevelopmentConfig, TestingConfig, ProductionConfig


app = Flask(__name__,
            static_url_path='',
            static_folder='static',
            template_folder='templates'
            )

if app.config['ENV'] == "production":
    app.config.from_object(ProductionConfig)
elif app.config['ENV'] == "testing":
    app.config.from_object(TestingConfig)
else:
    app.config.from_object(DevelopmentConfig())

db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app, db)
mail = Mail(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

from lps.seeds import seed_database, export_seed
from lps.schemas import *
from lps.models import *
from lps.forms import *


# Decorator for API check
def api_key_required(func):
    wraps(func)
    def wrapper(*args, **kwargs):
        api_key_header = request.headers.get('X-Api-Key')
        if api_key_header is None:
            abort(401)
        
        api_key = ApiKey.query.filter_by(api_key=api_key_header).first()
        if api_key is None:
            abort(401)

        if api_key.expired_at <= datetime.now():
            abort(401)

        return func(*args, **kwargs)
    
    wrapper.__name__ = func.__name__
    return wrapper


# DATABASE COMMANDS
@app.cli.command("seed_db")
def seed_db():
    print("======== STARTING DATABASE SEED ========")
    seed_database(db)
    print("======== SEED COMPLETED ========")


@app.cli.command("reset_db")
def reset_db():
    LocatorPoint.query.delete()
    Unit.query.delete()
    ApiKey.query.delete()
    User.query.delete()
    db.session.commit()
    print("======== RESET DATABASE ========")


@app.cli.command("export_db")
def export_db():
    print("======== EXPORTING DATABASE SEED ========")
    export_seed()
    print("======== EXPORT COMPLETED ========")


# MAIL SERVER COMMANDS
@app.cli.command("test_mail")
def test_mail():
    msg = Message("This is a testing email from the LPS Platform!", sender="admin@lps.com", recipients=["fer.leira@hotmail.com"])
    mail.send(msg)


# LOGIN MANAGER ROUTES
@login_manager.user_loader
def load_user(email):
    if email is not None:
        User.query.filter_by(email=email).first()
    return None


@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    flash('You must be logged in to view that page.')
    return redirect(url_for('login'))


# VIEW ROUTES
@app.route('/', methods=["GET"])
def index():
    return render_template('index.html'), 200


@app.route('/login', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password_hash(form.password.data):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Invalid Username')
            return redirect(url_for('login'))

    return render_template('login.html', form=form)


@app.route('/signup', methods=["GET", "POST"])
def signup():
    return "Signup"


@app.route('/logout', methods=["GET", "POST"])
def logout():
    return "Logout"


@app.route('/map', methods=["GET"])
@login_required
def map():
    units_q = Unit.query.all()
    units = UnitSchema(many=True).dump(units_q)

    return render_template('map.html', units=units, google_api_key=app.config['GOOGLE_CLOUD_API_KEY']), 200


# API ROUTES
@app.route('/api/locators', methods=["GET", "POST", "PUT", "DELETE"])
#@api_key_required
def locators():
    if request.method == "POST":
        new_point = LocatorPoint(
            request.form['title'],
            request.form['description'],
            request.form['point_type'],
            float(request.form['lat']),
            float(request.form['lon']),
            request.form['unit_id']
        )

        db.session.add(new_point)
        db.session.commit()
        return jsonify(message="Point {point_id} has been inserted.".format(point_id=new_point.point_id)), 201
    else:  # GET
        points_q = LocatorPoint.query.all()
        points = LocatorPointSchema(many=True).dump(points_q)
        return jsonify(points), 200


@app.route('/api/units', methods=["GET", "POST", "PUT", "DELETE"])
def units():
    if request.method == "POST":
        new_unit = Unit(
            request.form['name']
        )

        db.session.add(new_unit)
        db.session.commit()
        return jsonify(message="Unit {unit_id} has been inserted.".format(unit_id=new_unit.unit_id)), 201
    else:  # GET
        units_q = Unit.query.all()
        units = UnitSchema(many=True).dump(units_q)
        return jsonify(units), 200
