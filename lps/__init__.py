from instance.config import GOOGLE_CLOUD_API_KEY
from flask import Flask, render_template, request, jsonify, abort, url_for
from flask.wrappers import Request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate

from lps.config import Config


app = Flask(__name__,
            static_url_path='',
            static_folder='static',
            template_folder='templates'
)
app.config.from_object(Config)

Bootstrap(app)

db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app, db)

from lps.models import *
from lps.schemas import *

@app.route('/', methods=["GET"])
def home():
    return render_template('index.html', google_api_key=GOOGLE_CLOUD_API_KEY)

@app.route('/locators', methods=["GET", "POST"])
def locators():
    if request.method == "GET":
        # TODO
        return jsonify(tags='TBD')
    else:
        pass
