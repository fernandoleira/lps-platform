from flask import Flask, render_template, request, jsonify, abort, url_for, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_cors import CORS
from instance.config import DevelopmentConfig, TestingConfig, ProductionConfig


app = Flask(__name__,
            static_url_path='',
            static_folder='static',
            template_folder='templates'
            )
app.config.from_object(TestingConfig)

db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app, db)
CORS(app)

from lps.seeds import seed_database, export_seed
from lps.schemas import *
from lps.models import *


@app.cli.command("seed_db")
def seed_db():
    print("======== STARTING DATABASE SEED ========")
    seed_database(db)
    print("======== SEED COMPLETED ========")


@app.cli.command("reset_db")
def reset_db():
    LocatorPoint.query.delete()
    Unit.query.delete()
    db.session.commit()
    print()


@app.cli.command("export_db")
def export_db():
    print("======== EXPORTING DATABASE SEED ========")
    export_seed()
    print("======== EXPORT COMPLETED ========")


@app.route('/', methods=["GET"])
def home():
    units_q = Unit.query.all()
    units = UnitSchema(many=True).dump(units_q)

    return render_template('index.html', units=units, google_api_key=app.config['GOOGLE_CLOUD_API_KEY']), 200


@app.route('/locators', methods=["GET", "POST", "PUT", "DELETE"])
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


@app.route('/units', methods=["GET", "POST", "PUT", "DELETE"])
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
