import os
from flask import Flask, render_template, request, jsonify, abort, url_for, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate

from lps.config import Config
from instance.config import GOOGLE_CLOUD_API_KEY


app = Flask(__name__,
            static_url_path='',
            static_folder='static',
            template_folder='templates'
)
app.config.from_object(Config)

db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app, db)

from lps.models import *
from lps.schemas import *
from lps.seeds import seed_database


@app.cli.command("seed_db")
def seed_db():
    seed_database(db)

@app.cli.command("reset_db")
def reset_db():
    LocatorPoint.query.delete()
    Unit.query.delete()
    db.session.commit()

@app.route('/', methods=["GET"])
def home():
    return render_template('index.html', google_api_key=GOOGLE_CLOUD_API_KEY), 200

@app.route('/locators', methods=["GET", "POST"])
def locators():
    if request.method == "GET":
        q = LocatorPoint.query.all()
        res = LocatorPointSchema(many=True).dump(q)
        return jsonify(res)

    else: # POST
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
