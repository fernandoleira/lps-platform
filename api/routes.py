import datetime
import jwt
from threading import Thread
from flask import (Blueprint, jsonify, request, current_app,
                   copy_current_request_context, render_template)
from werkzeug.security import generate_password_hash
from api import db
from api.models import LocatorPoint, Unit, User
from api.schemas import LocatorPointSchema, UnitSchema, UserSchema
from api.mail import send_alert_mail
from api.sms import send_alert_sms
from api.utils import api_key_required


api_bp = Blueprint("api_bp", __name__, url_prefix="/api/v1",
                   static_folder="static")


# HOME ROUTES
@api_bp.route('/', methods=["GET"])
def home():
    metadata = {
        'title': "Locator Pointer System (LPS)",
        'description': "This is the api project for the LPS platform server backend",
        'author_name': "Fernando Leira Cortel",
        'author_email': "LeiraFernandoCortel@gmail.com",
        'source': "https://github.com/fernandoleira/lps-platform",
        'license': "MIT"
    }

    return jsonify(metadata), 200


# API ROUTES
@api_bp.route('/locators', methods=["GET", "POST"])
# @api_key_required
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

        if request.form['point_id'] is not None:
            new_point.point_id = request.form['point_id']

        db.session.add(new_point)
        db.session.commit()

        # If new point received is an alert, send an email and/or sms notification to the User
        if new_point.point_type == "Alert":
            @copy_current_request_context
            def alert_mail():
                send_alert_mail(new_point, new_point.unit.user)

            @copy_current_request_context
            def alert_sms():
                send_alert_sms(new_point, new_point.unit.user)

            if new_point.unit.alert_mail:
                Thread(target=alert_mail).start()
            if new_point.unit.alert_sms:
                Thread(target=alert_sms).start()

        return jsonify(
            message=f"Point {new_point.point_id} has been inserted.",
            point_id=new_point.point_id
        ), 201

    else:  # GET
        points_q = LocatorPoint.query.all()
        points = LocatorPointSchema(many=True).dump(points_q)

        return jsonify(points), 200


@api_bp.route('/locators/<string:point_id>', methods=["GET", "PUT", "DELETE"])
# @api_key_required
def locator(point_id):
    point = LocatorPoint.query.filter_by(point_id=point_id).first()
    if point:
        if request.method == "PUT":
            point.title = request.form['title']
            point.description = request.form['description']
            point.point_type = request.form['point_type']
            point.lat = request.form['lat']
            point.lon = request.form['lon']
            db.session.commit()
            return jsonify(message=f"Point {point_id} has been updated."), 200

        elif request.method == "DELETE":
            db.session.delete(point)
            db.session.commit()
            return jsonify(message=f"Point {point_id} has been deleted."), 200

        else:
            res = LocatorPointSchema().dump(point)
            return jsonify(res), 200

    elif point_id is not None:
        return jsonify(error=f"Point {point_id} does not exist."), 404

    else:
        return jsonify(error="Point id is required."), 406


@api_bp.route('/units', methods=["GET", "POST"])
# @api_key_required
def units():
    if request.method == "POST":
        if 'unit_id' in request.form.keys():
            req_unit_id = request.form['unit_id']
        else:
            req_unit_id = None

        req_alert_mail = True if request.form['alert_mail'] == 'true' else False
        req_alert_sms = True if request.form['alert_sms'] == 'true' else False

        new_unit = Unit(
            request.form['name'],
            request.form['user_id'],
            req_alert_mail,
            req_alert_sms,
            unit_id=req_unit_id
        )

        db.session.add(new_unit)
        db.session.commit()
        return jsonify(
            message=f"Unit {new_unit.unit_id} has been inserted.",
            unit_id=new_unit.unit_id
        ), 201

    else:  # GET
        units_q = Unit.query.all()
        units = UnitSchema(many=True).dump(units_q)
        return jsonify(units), 200


@api_bp.route('/units/<string:unit_id>', methods=["GET", "PUT", "DELETE"])
# @api_key_required
def unit(unit_id):
    unit = Unit.query.filter_by(unit_id=unit_id).first()
    if unit:
        if request.method == "PUT":
            unit.name = request.form['name']
            db.session.commit()
            return jsonify(message=f"Unit {unit_id} has been updated."), 200

        elif request.method == "DELETE":
            db.session.delete(unit)
            db.session.commit()
            return jsonify(message=f"Unit {unit_id} has been deleted."), 200

        else:
            res = UnitSchema().dump(unit)
            return jsonify(res), 200

    elif unit_id is not None:
        return jsonify(error=f"Unit {unit_id} does not exist."), 404

    else:
        return jsonify(error="Unit id is required."), 406


@api_bp.route('/users', methods=["GET", "POST"])
def users():
    if request.method == "POST":
        new_user = User(
            request.form['username'],
            request.form['email'],
            request.form['phone_number'],
            request.form['password']
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify(
            message=f"User {new_user.user_id} has been inserted.",
            user_id=new_user.user_id
        ), 201

    else:  # GET
        users_q = User.query.all()
        users = UserSchema(many=True).dump(users_q)
        return jsonify(users), 200


@api_bp.route('/users/<string:username>', methods=["GET", "PUT", "DELETE"])
def user(username):
    user = User.query.filter_by(username=username).first()
    if user:
        if request.method == "PUT":
            user.username = request.form['username']
            user.email = request.form['email']
            user.phone_number = request.form['phone_number']
            user.pswd_hash = generate_password_hash(request.form['password'])
            db.session.commit()
            return jsonify(message=f"User {user.user_id} has been updated."), 200

        elif request.method == "DELETE":
            db.session.delete(user)
            db.session.commit()
            return jsonify(message=f"User {user.user_id} has been deleted."), 200

        else:  # GET
            return jsonify(UserSchema().dump(user)), 200

    elif username is not None:
        return jsonify(error=f"User {username} does not exist."), 406

    else:
        return jsonify(error=f"User Id is required."), 406


# AUTH ROUTES
@api_bp.route('/login', methods=["POST"])
def login():
    user_q = User.query.filter_by(email=request.form['email']).first()
    if user_q:
        user = UserSchema().dump(user_q)
        if user_q.check_password_hash(request.form['password']):
            tocken = jwt.encode(
                {
                    'user_id': user['user_id'],
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
                },
                current_app.secret_key,
                "HS256")

            return jsonify(tocken=tocken), 200

    return jsonify(error=f"User with email {request.form['email']} does not exist or password is incorrect."), 401


@api_bp.route('/logout', methods=["DELETE"])
def logout():
    # TODO
    pass


# SWAGGER DOCUMENTATION ROUTE
@api_bp.route('/swagger', methods=["GET"])
def swagger():
    return render_template("swaggerui.html")
