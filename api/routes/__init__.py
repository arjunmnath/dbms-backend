from flask import Blueprint

appbp = Blueprint('appbp', __name__)

from . import user, category, product, order, bid, review, messages

# def register_blueprints(app):
    # app.register_blueprint(appbp)