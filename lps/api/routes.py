from functools import wraps
from datetime import datetime
from flask import Blueprint, jsonify, request, abort
from lps import db
from lps.models import LocatorPoint, Unit, ApiKey
from lps.schemas import LocatorPointSchema, UnitSchema
from lps.mail import send_alert_mail


api_bp = Blueprint("api_bp", __name__, url_prefix="/api")


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


# API ROUTES
@api_bp.route('/locators', methods=["GET", "POST"])
@api_key_required
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


@api_bp.route('/locators/<string:point_id>', methods=["GET", "PUT", "DELETE"])
@api_key_required
def locator(point_id):
    point = LocatorPoint.query.filter_by(point_id=point_id).first()
    if point:
        if request.method == "PUT":
            point.title = request.form['title']
            point.description = request.form['description']
            point.point_type = request.form['point_type']
            point.lat = request.form['lat']
            point.lon = request.form['lon']
            point.unit_id = request.form['unit_id']
            db.session.commit()
            return jsonify(message="Point {point_id} has been updated.".format(point_id=point_id)), 201
        elif request.method == "DELETE":
            db.session.delete(point)
            db.session.commit()
            return jsonify(message="Point {point_id} has been deleted.".format(point_id=point_id)), 201
        else:
            res = LocatorPointSchema().dump(point)
            return jsonify(res), 200
    elif point_id is not None:
        return jsonify(error="Point {point_id} does not exist.".format(point_id=point_id)), 404
    else:
        return jsonify(error="Point id is required."), 406


@api_bp.route('/units', methods=["GET", "POST"])
@api_key_required
def units():
    if request.method == "POST":
        new_unit = Unit(
            request.form['name'],
            request.form['user_id']
        )

        db.session.add(new_unit)
        db.session.commit()
        return jsonify(message="Unit {unit_id} has been inserted.".format(unit_id=new_unit.unit_id)), 201
    else:  # GET
        units_q = Unit.query.all()
        units = UnitSchema(many=True).dump(units_q)
        return jsonify(units), 200


@api_bp.route('/units/<string:unit_id>', methods=["GET", "PUT", "DELETE"])
@api_key_required
def unit(unit_id):
    unit = Unit.query.filter_by(unit_id=unit_id).first()
    if unit:
        if request.method == "PUT":
            unit.name = request.form['name']
            db.session.commit()
            return jsonify(message="Unit {unit_id} has been updated.".format(unit_id=unit_id)), 201
        elif request.method == "DELETE":
            db.session.delete(unit)
            db.session.commit()
            return jsonify(message="Unit {unit_id} has been deleted.".format(unit_id=unit_id)), 201
        else:
            res = UnitSchema().dump(unit)
            return jsonify(res), 200
    elif unit_id is not None:
        return jsonify(error="Unit {unit_id} does not exist.".format(unit_id=unit_id)), 404
    else:
        return jsonify(error="Unit id is required."), 406
