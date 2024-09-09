from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

app = Flask(__name__)
app.config.from_object('api.config.Config')

db.init_app(app)

with app.app_context():
    # from routes import register_blueprints
    from api.routes import appbp
    # routes.register_blueprints(app)
    app.register_blueprint(appbp)

    db.create_all()

