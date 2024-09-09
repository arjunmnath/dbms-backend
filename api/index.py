from flask import Flask
from api.routes import appbp
from api.models import db

app = Flask(__name__)
app.config.from_object('api.config.Config')

db.init_app(app)

with app.app_context():
    app.register_blueprint(appbp)
    db.create_all()

