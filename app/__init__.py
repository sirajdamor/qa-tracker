from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app(config=None):
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tracker.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    if config:
        app.config.update(config)

    db.init_app(app)

    from .routes import bp
    app.register_blueprint(bp)

    with app.app_context():
        db.create_all()
        if not app.config.get("TESTING"):
            seed_data()

    return app


def seed_data():
    from .models import Bug
    if Bug.query.count() == 0:
        db.session.add_all([
            Bug(title="Login button not responding", severity="High", status="Open"),
            Bug(title="Typo on dashboard heading", severity="Low", status="Resolved"),
            Bug(title="Report export crashes on empty data", severity="Critical", status="In Progress"),
        ])
        db.session.commit()
