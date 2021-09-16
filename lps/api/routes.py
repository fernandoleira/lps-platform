from functools import wraps
from flask import Blueprint, jsonify, request
from lps import db
from lps.models import LocatorPoint, Unit, ApiKey
from lps.schemas import LocatorPointSchema, UnitSchema


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
@api_bp.route('/locators', methods=["GET", "POST", "PUT", "DELETE"])
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


@api_bp.route('/units', methods=["GET", "POST", "PUT", "DELETE"])
#@api_key_required
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
