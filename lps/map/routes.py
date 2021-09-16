from flask import Blueprint, current_app, render_template
from flask_login import login_required
from lps.models import Unit
from lps.schemas import UnitSchema

map_bp = Blueprint("map_bp", __name__, url_prefix="/map", template_folder="templates")

@map_bp.route('/', methods=["GET"])
@login_required
def map():
    units_q = Unit.query.all()
    units = UnitSchema(many=True).dump(units_q)

    return render_template('map.html', units=units, google_api_key=current_app.config['GOOGLE_CLOUD_API_KEY']), 200
