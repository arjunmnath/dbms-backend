import os

from flask import Flask
from api.routes import appbp
from api.models import db
import pymysql
pymysql.install_as_MySQLdb()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.urandom(24)
db.init_app(app)
with app.app_context():
    app.register_blueprint(appbp)
    db.create_all()

