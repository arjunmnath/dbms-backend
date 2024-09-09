from flask import Blueprint

appbp = Blueprint('appbp', __name__)

from api.routes import *

# def register_blueprints(app):
    # app.register_blueprint(appbp)