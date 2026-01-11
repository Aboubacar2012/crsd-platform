from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    # --------------------
    # Identité
    # --------------------
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)

    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(50), nullable=False)

    # --------------------
    # Organisation (RELATIONNEL)
    # --------------------
    actor_type_id = db.Column(
        db.Integer,
        db.ForeignKey("actor_types.id"),
        nullable=False
    )

    organisation_id = db.Column(
        db.Integer,
        db.ForeignKey("organisations.id"),
        nullable=False
    )

    actor_type = db.relationship("ActorType", lazy=True)
    organisation = db.relationship("Organisation", lazy=True)

    # --------------------
    # Rôle utilisateur
    # --------------------
    role = db.Column(
        db.String(20),
        nullable=False,
        default="USER"   # USER | ADMIN
    )

    # --------------------
    # Sécurité
    # --------------------
    password_hash = db.Column(db.String(255), nullable=False)

    # --------------------
    # Password helpers
    # --------------------
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # --------------------
    # Role helpers
    # --------------------
    def is_admin(self):
        return self.role == "ADMIN"

    def __repr__(self):
        return f"<User {self.email} ({self.role})>"
