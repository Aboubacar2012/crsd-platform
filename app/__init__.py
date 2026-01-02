import os
from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from app.config import Config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "auth.login"

def create_app():
    # 🔴 CHEMINS ABSOLUS (clé du problème)
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    app = Flask(
        __name__,
        template_folder=os.path.join(BASE_DIR, "templates"),
        static_folder=os.path.join(BASE_DIR, "static"),
    )

    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    
    # =========================
    # BLUEPRINTS
    # =========================

    from app.auth.routes import auth_bp
    from app.home.routes import home_bp
    from app.admin.routes import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(home_bp)
    app.register_blueprint(admin_bp)

    with app.app_context():
        db.create_all()

    @app.route("/")
    def index():
        return redirect(url_for("auth.login"))

    return app
