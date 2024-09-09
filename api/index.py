from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)

    with app.app_context():
        # from routes import register_blueprints
        from routes import appbp
        # routes.register_blueprints(app)
        app.register_blueprint(appbp)

        db.create_all()
        

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)