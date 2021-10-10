from threading import Thread
from flask import Blueprint, jsonify, request, copy_current_request_context
from lps import db
from lps.models import LocatorPoint, Unit
from lps.schemas import LocatorPointSchema, UnitSchema
from lps.mail_utils import send_alert_mail
from lps.sms import send_alert_sms
from lps.api.utils import api_key_required


api_bp = Blueprint("api_bp", __name__, url_prefix="/api")


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

            if new_point.unit.alert_mail == None:
                Thread(target=alert_mail).start()
            if new_point.unit.alert_sms:
                Thread(target=alert_sms).start()
            
        
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
