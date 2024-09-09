from flask import Blueprint

appbp = Blueprint('appbp', __name__)

from api.routes import  bid, category, messages, order, product, review, user
