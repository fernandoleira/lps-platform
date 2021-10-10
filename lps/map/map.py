from flask import Blueprint, current_app, render_template, jsonify
from flask_login import login_required
from lps.models import Unit, LocatorPoint
from lps.schemas import UnitSchema, LocatorPointSchema


map_bp = Blueprint("map_bp", __name__, url_prefix="/map", template_folder="templates")


@map_bp.route('/', methods=["GET"])
@login_required
def map():
    units_q = Unit.query.all()
    units = UnitSchema(many=True).dump(units_q)

    return render_template('map.html', units=units, google_api_key=current_app.config['GOOGLE_CLOUD_API_KEY']), 200


@map_bp.route('/locators', methods=["GET"])
@login_required
def map_locators():
    points_q = LocatorPoint.query.all()
    points = LocatorPointSchema(many=True).dump(points_q)
    return jsonify(points), 200
