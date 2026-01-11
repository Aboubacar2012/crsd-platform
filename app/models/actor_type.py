from app import db


class ActorType(db.Model):
    __tablename__ = "actor_types"

    id = db.Column(db.Integer, primary_key=True)

    # Code court : ONG, PTF, ETAT, BILATERAL, etc.
    code = db.Column(db.String(50), unique=True, nullable=False)

    # Libellé lisible
    label = db.Column(db.String(150), nullable=False)

    description = db.Column(db.Text)

    # Actif / inactif (meilleure pratique que supprimer)
    is_active = db.Column(db.Boolean, default=True)

    created_at = db.Column(
        db.DateTime, server_default=db.func.now()
    )

    updated_at = db.Column(
        db.DateTime,
        server_default=db.func.now(),
        onupdate=db.func.now()
    )

    # Relation avec organisations
    organisations = db.relationship(
        "Organisation",
        backref="actor_type",
        lazy=True,
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<ActorType {self.code}>"
