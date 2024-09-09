from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    try:
        db.init_app(app)
    except Exception as e:
        print(f"Error initializing database: {e}")

    with app.app_context():
        # from routes import register_blueprints
        import routes
        routes.register_blueprints(app)
        try:
            db.create_all()
        except Exception as e:
            print(f"Error creating tables: {e}")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)